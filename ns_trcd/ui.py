import numpy as np
import structlog
from pathlib import Path
from pyqtgraph import ViewBox
from PySide2.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PySide2.QtCore import QObject, QThread, Signal, Slot, QMutex
from . import common
from .common import PlotData, UiSettings
from .comp_worker import ComputationWorker
from .exp_worker import ExperimentWorker
from .generated_ui import Ui_MainWindow


logger = structlog.get_logger()


class MainWindowSignals(QObject):
    measure = Signal()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.signals = MainWindowSignals()
        self._log = logger.bind(worker="main")
        log = self._log.bind(method="__init__")
        self.save_data_dir = None
        self.current_measurement = 0
        self.max_measurements = 0
        self.collecting = False
        self.time_axis = None
        self.mutex = QMutex()
        self.comp_thread = QThread()
        self.exp_thread = QThread()
        log.debug("threads created")
        self._connect_components()
        log.debug("components connected")
        self._set_initial_widget_states()
        log.debug("initial states set")
        self._store_line_objects()
        log.debug("graph objects stored")
        self._set_plot_mouse_mode()
        log.debug("mouse mode set")

    def _set_initial_widget_states(self):
        self.update_max_measurements(self.ui.measurements.value())
        self.ui.stop_btn.setDisabled(True)
        self.ui.reset_avg_btn.setDisabled(True)
        self.ui.save_loc.setDisabled(True)
        self.ui.save_loc_browse_btn.setDisabled(True)

    def _connect_components(self):
        """Connect widgets and events to make the UI respond to user interaction.
        """
        # Start/Stop Buttons
        self.ui.start_btn.clicked.connect(self.start_collecting)
        self.ui.stop_btn.clicked.connect(self.stop_collecting)
        # Measurement Counter
        self.ui.measurements.valueChanged.connect(self.update_max_measurements)
        # Save data controls
        self.ui.save_data_checkbox.stateChanged.connect(self.save_loc_set_state)
        self.ui.save_loc_browse_btn.clicked.connect(self.get_save_location)
        # Start/Stop point
        self.ui.stop_pt_checkbox.stateChanged.connect(self.stop_pt_set_state)
        # Dark current
        self.ui.dark_curr_checkbox.stateChanged.connect(self.dark_curr_set_state)

    def closeEvent(self, event):
        """Clean up worker threads if the window is closed while collecting data.

        Notes
        -----
        This overrides the default closeEvent method of QMainWindow.
        """
        log = self._log.bind(method="closeEvent")
        if self.collecting:
            log.debug("quitting worker threads")
            self.comp_thread.quit()
            self.exp_thread.quit()
            log.debug("waiting computation thread")
            self.comp_thread.wait()
            log.debug("waiting for experiment thread")
            self.exp_thread.wait()
            log.debug("done waiting")
        event.accept()
        log.debug("exiting application")

    def _store_line_objects(self):
        """Store references to the lines so the data can be updated later.
        """
        starting_data = (np.arange(100), np.zeros(100))
        self.live_par_line = self.ui.live_par_graph.plot(*starting_data)
        self.live_perp_line = self.ui.live_perp_graph.plot(*starting_data)
        self.live_ref_line = self.ui.live_ref_graph.plot(*starting_data)
        self.live_da_par_line = self.ui.live_da_par_graph.plot(*starting_data)
        self.live_da_perp_line = self.ui.live_da_perp_graph.plot(*starting_data)
        self.live_da_cd_line = self.ui.live_da_cd_graph.plot(*starting_data)
        self.avg_da_par_line = self.ui.avg_da_par_graph.plot(*starting_data)
        self.avg_da_perp_line = self.ui.avg_da_perp_graph.plot(*starting_data)
        self.avg_da_cd_line = self.ui.avg_da_cd_graph.plot(*starting_data)

    def _set_plot_mouse_mode(self):
        self.ui.live_par_graph.getPlotItem().getViewBox().setMouseMode(ViewBox.RectMode)
        self.ui.live_perp_graph.getPlotItem().getViewBox().setMouseMode(
            ViewBox.RectMode
        )
        self.ui.live_ref_graph.getPlotItem().getViewBox().setMouseMode(ViewBox.RectMode)
        self.ui.live_da_par_graph.getPlotItem().getViewBox().setMouseMode(
            ViewBox.RectMode
        )
        self.ui.live_da_perp_graph.getPlotItem().getViewBox().setMouseMode(
            ViewBox.RectMode
        )
        self.ui.live_da_cd_graph.getPlotItem().getViewBox().setMouseMode(
            ViewBox.RectMode
        )
        self.ui.avg_da_par_graph.getPlotItem().getViewBox().setMouseMode(
            ViewBox.RectMode
        )
        self.ui.avg_da_perp_graph.getPlotItem().getViewBox().setMouseMode(
            ViewBox.RectMode
        )
        self.ui.avg_da_cd_graph.getPlotItem().getViewBox().setMouseMode(
            ViewBox.RectMode
        )

    @Slot(np.ndarray)
    def set_time_axis(self, values):
        log = self._log.bind(method="set_time_axis")
        self.time_axis = values * 1e6
        log.debug("time axis constructed")

    @Slot(int)
    def update_max_measurements(self, x):
        log = self._log.bind(method="update_max_measurements")
        self.max_measurements = x
        self.ui.measurement_counter_label.setText(
            f"{self.current_measurement}/{self.max_measurements}"
        )
        log.debug(f"max measurements is now {x}")

    @Slot(int)
    def update_current_measurement(self, x):
        log = self._log.bind(method="update_current_measurement")
        self.current_measurement = x
        self.ui.measurement_counter_label.setText(
            f"{self.current_measurement}/{self.max_measurements}"
        )
        log.debug(f"measurement {x}")

    @Slot()
    def start_collecting(self):
        """Begins collecting data when the "Start" button is pressed.
        """
        log = self._log.bind(method="start_collecting")
        settings, should_quit = self._collect_settings()
        log.debug("settings collected", should_quit=should_quit, settings=settings)
        if should_quit:
            log.debug("aborting experiment")
            return
        self.comp_worker = ComputationWorker(self.mutex, settings)
        self.exp_worker = ExperimentWorker(self.mutex, settings)
        log.debug("workers created")
        self._connect_worker_signals()
        log.debug("signals connected")
        self.comp_worker.moveToThread(self.comp_thread)
        self.exp_worker.moveToThread(self.exp_thread)
        log.debug("workers moved to separate threads")
        self.comp_thread.start()
        self.exp_thread.start()
        log.debug("worker threads started")
        self.signals.measure.emit()
        log.debug("measure signal emitted")
        self._disable_acq_controls()
        log.debug("controls disabled")

    def _collect_settings(self):
        """Collect all the settings from the UI.
        """
        log = self._log.bind(method="_collect_settings")
        settings = UiSettings()
        settings, should_quit = self._collect_meas_settings(settings)
        log.debug("measurement settings", settings=settings, should_quit=should_quit)
        if should_quit:
            return settings, should_quit
        settings, should_quit = self._collect_instr_settings(settings)
        log.debug("instrument settings", settings=settings, should_quit=should_quit)
        if should_quit:
            return settings, should_quit
        settings, should_quit = self._collect_save_settings(settings)
        log.debug("save settings", settings=settings, should_quit=should_quit)
        if should_quit:
            return settings, should_quit
        settings, should_quit = self._collect_start_stop_settings(settings)
        log.debug("start/stop settings", settings=settings, should_quit=should_quit)
        if should_quit:
            return settings, should_quit
        settings, should_quit = self._collect_dark_curr_settings(settings)
        log.debug("dark current settings", settings=settings, should_quit=should_quit)
        return settings, should_quit

    def _collect_dark_curr_settings(self, settings):
        log = self._log.bind(method="_collect_dark_curr_settings")
        quit = False
        use_dark_curr = self.ui.dark_curr_checkbox.isChecked()
        log.debug("dark current checkbox", checked=use_dark_curr)
        if not use_dark_curr:
            return settings, quit
        try:
            dark_curr_par = float(self.ui.dark_curr_par.text())
            dark_curr_perp = float(self.ui.dark_curr_perp.text())
            dark_curr_ref = float(self.ui.dark_curr_ref.text())
            settings.dark_curr_par = dark_curr_par
            settings.dark_curr_perp = dark_curr_perp
            settings.dark_curr_ref = dark_curr_ref
        except ValueError:
            quit = True
        return settings, quit

    def _collect_meas_settings(self, settings):
        """Collect the number of measurements from the UI.
        """
        quit = False
        settings.num_measurements = self.ui.measurements.value()
        return settings, quit

    def _collect_instr_settings(self, settings):
        """Collect the settings from the UI related to the instrument.
        """
        quit = False
        instr_name = self.ui.instr_name.text()
        if instr_name == "":
            quit = True
        settings.instr_name = instr_name
        return settings, quit

    def _collect_save_settings(self, settings):
        """Collect the settings from the UI related to saving data.
        """
        log = self._log.bind(method="_collect_save_settings")
        quit = False
        should_save = self.ui.save_data_checkbox.isChecked()
        log.debug("save checkbox", checked=should_save)
        if should_save and not self._saving_should_proceed():
            quit = True
        settings.save = should_save
        settings.save_loc = self.ui.save_loc.text()
        return settings, quit

    def _collect_start_stop_settings(self, settings):
        """Collect the settings from the UI related to the Start/Stop points.
        """
        quit = False
        start_pt = self.ui.start_pt.value()
        settings.start_pt = start_pt
        if not self.ui.stop_pt_checkbox.isChecked():
            stop_pt = self.ui.stop_pt.value()
            settings.stop_pt = stop_pt
            if start_pt >= stop_pt:
                self._tell_start_greater_than_stop()
                quit = True
        return settings, quit

    def _connect_worker_signals(self):
        """Connect signals for communication between workers and the main window.
        """
        # Produced by the experiment worker
        self.exp_worker.signals.preamble.connect(self.comp_worker.store_preamble)
        self.exp_worker.signals.new_data.connect(self.comp_worker.compute_signals)
        self.exp_worker.signals.done.connect(self.cleanup_when_done)
        # Produced by the computation worker
        self.comp_worker.signals.time_axis.connect(self.set_time_axis)
        self.comp_worker.signals.new_data.connect(self.update_plots)
        self.comp_worker.signals.meas_num.connect(self.update_current_measurement)
        # Produced by the main window
        self.signals.measure.connect(self.exp_worker.measure)
        self.ui.reset_avg_btn.clicked.connect(self.comp_worker.reset_averages)

    def _disable_acq_controls(self):
        """Disable certain controls while collecting data.
        """
        # Disabled
        self.ui.start_btn.setDisabled(True)
        self.ui.instr_name.setDisabled(True)
        self.ui.measurements.setDisabled(True)
        self.ui.save_data_checkbox.setDisabled(True)
        self.ui.save_loc.setDisabled(True)
        self.ui.save_loc_browse_btn.setDisabled(True)
        self.ui.start_pt.setDisabled(True)
        self.ui.stop_pt.setDisabled(True)
        self.ui.stop_pt_checkbox.setDisabled(True)
        # Enabled
        self.ui.stop_btn.setEnabled(True)
        self.ui.reset_avg_btn.setEnabled(True)

    def _enable_acq_controls(self):
        """Enable certain controls after data collection is complete.
        """
        # Enabled
        self.ui.start_btn.setEnabled(True)
        self.ui.instr_name.setEnabled(True)
        self.ui.measurements.setEnabled(True)
        self.ui.save_data_checkbox.setEnabled(True)
        if self.ui.save_data_checkbox.isChecked():
            self.ui.save_loc.setEnabled(True)
            self.ui.save_loc_browse_btn.setEnabled(True)
        self.ui.start_pt.setEnabled(True)
        self.ui.stop_pt_checkbox.setEnabled(True)
        if not self.ui.stop_pt_checkbox.isChecked():
            self.ui.stop_pt.setEnabled(True)
        # Disabled
        self.ui.stop_btn.setDisabled(True)
        self.ui.reset_avg_btn.setDisabled(True)

    @Slot()
    def stop_collecting(self):
        """Stops collecting data when the "Stop" button is pressed.
        """
        log = self._log.bind(method="stop_collecting")
        log.debug("stop button clicked")
        self.mutex.lock()
        log.debug("mutex locked")
        common.SHOULD_STOP = True
        self.mutex.unlock()
        log.debug("mutex unlocked")
        log.debug("quitting worker threads")
        self.comp_thread.quit()
        self.exp_thread.quit()
        log.debug("waiting for computation thread")
        self.comp_thread.wait()
        log.debug("waiting for experiment thread")
        self.exp_thread.wait()
        log.debug("done waiting")
        self._enable_acq_controls()
        log.debug("controls enabled")
        self.current_measurement = 0

    @Slot()
    def cleanup_when_done(self):
        """Clean up workers and threads after data collection is complete.
        """
        log = self._log.bind(method="cleanup_when_done")
        log.debug("quitting worker threads")
        self.comp_thread.quit()
        self.exp_thread.quit()
        log.debug("waiting for computation thread")
        self.comp_thread.wait()
        log.debug("waiting for experiment thread")
        self.exp_thread.wait()
        log.debug("done waiting")
        self.mutex.lock()
        log.debug("mutex locked")
        common.SHOULD_STOP = False
        self.mutex.unlock()
        log.debug("mutex unlocked")
        self._enable_acq_controls()
        log.debug("controls enabled")
        self.current_measurement = 0
        log.debug("presenting dialog")
        QMessageBox.information(
            self, "Done", "The experiment has finished.", QMessageBox.StandardButton.Ok
        )
        log.debug("dialog dismissed")

    @Slot(PlotData)
    def update_plots(self, data):
        """Update the plots in the Live/Average tabs when new data is available.

        Parameters
        ----------
        data : PlotData
            Three live data channels and the signals computed from them.
        """
        log = self._log.bind(method="update_plots")
        self.live_par_line.setData(self.time_axis, data.par)
        self.live_perp_line.setData(self.time_axis, data.perp)
        self.live_ref_line.setData(self.time_axis, data.ref)
        log.debug("raw signals updated")
        if data.da_par is not None:
            self.live_da_par_line.setData(self.time_axis, data.da_par)
            self.live_da_perp_line.setData(self.time_axis, data.da_perp)
            self.live_da_cd_line.setData(self.time_axis, data.da_cd)
            self.avg_da_par_line.setData(self.time_axis, data.avg_da_par)
            self.avg_da_perp_line.setData(self.time_axis, data.avg_da_perp)
            self.avg_da_cd_line.setData(self.time_axis, data.avg_da_cd)
            log.debug("da signals updated")

    @Slot(int)
    def save_loc_set_state(self, state):
        """Enable or disable the save location controls in response to the checkbox.

        Parameters
        ----------
        state : int
            An integer representing the state of the checkbox.

        Notes
        -----
            0 - unchecked
            2 - checked
        """
        log = self._log.bind(method="save_loc_set_state", state=state)
        if state == 0:
            self.ui.save_loc.setDisabled(True)
            self.ui.save_loc_browse_btn.setDisabled(True)
            log.debug("save data disabled")
        elif state == 2:
            self.ui.save_loc.setEnabled(True)
            self.ui.save_loc_browse_btn.setEnabled(True)
            log.debug("save data enabled")

    @Slot()
    def get_save_location(self):
        """Get an existing directory in which to store the collected data.
        """
        self.save_data_dir = QFileDialog.getExistingDirectory()
        self.ui.save_loc.setText(self.save_data_dir)

    def _save_loc_still_valid(self):
        save_dir = Path(self.save_data_dir)
        return save_dir.exists()

    def _tell_save_loc_is_invalid(self):
        """Tell the user that the current save location isn't valid or doesn't exist.
        """
        QMessageBox.critical(
            self,
            "Invalid Save Location",
            "The current save data location is invalid or doesn't exist. Please choose a new location.",
            QMessageBox.StandardButton.Ok,
        )

    def _save_would_overwrite(self):
        """Returns True if the save directory contains *anything*.
        """
        for item in Path(self.save_data_dir).iterdir():
            return True
        return False

    def _should_overwrite(self):
        """Asks the user whether data in the save directory should be overwritten.
        """
        reply = QMessageBox.warning(
            self,
            "Overwrite?",
            "The current directory contents will be erased. Continue?",
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel,
        )
        return reply == QMessageBox.StandardButton.Ok

    def _saving_should_proceed(self):
        """Determine whether valid settings have been entered for saving data.
        """
        log = self._log.bind(method="_saving_should_proceed")
        try:
            loc_is_valid = self._save_loc_still_valid()
            log.debug("save location", valid=loc_is_valid)
        except TypeError:
            loc_is_valid = False
            log.debug("save location", valid=loc_is_valid)
        if not loc_is_valid:
            self._tell_save_loc_is_invalid()
            return False
        would_overwrite = self._save_would_overwrite()
        log.debug("overwrite", would_overwrite=would_overwrite)
        if would_overwrite and (not self._should_overwrite()):
            return False
        return True

    @Slot(int)
    def stop_pt_set_state(self, state):
        """Enable or disable the "Stop Point" controls in response to the checkbox.

        Parameters
        ----------
        state : int
            An integer representing the state of the checkbox.

        Notes
        -----
            0 - unchecked
            2 - checked
        """
        log = self._log.bind(method="stop_pt_set_state", state=state)
        if state == 2:
            self.ui.stop_pt.setDisabled(True)
            log.debug("disabled")
        elif state == 0:
            self.ui.stop_pt.setEnabled(True)
            log.debug("enabled")

    def _tell_start_greater_than_stop(self):
        """Tell the user that the current save location isn't valid or doesn't exist.
        """
        QMessageBox.critical(
            self,
            "Invalid Start/Stop Points",
            "The Start point must be less than the Stop point.",
            QMessageBox.StandardButton.Ok,
        )

    @Slot(int)
    def dark_curr_set_state(self, state):
        """Enable or disable the dark current controls in response to the checkbox.

        Parameters
        ----------
        state : int
            An integer representing the state of the checkbox.

        Notes
        -----
            0 - unchecked
            2 - checked
        """
        log = self._log.bind(method="_collect_settings", state=state)
        if state == 0:
            self.ui.dark_curr_par.setDisabled(True)
            self.ui.dark_curr_perp.setDisabled(True)
            self.ui.dark_curr_ref.setDisabled(True)
            log.debug("disabled")
        elif state == 2:
            self.ui.dark_curr_par.setEnabled(True)
            self.ui.dark_curr_perp.setEnabled(True)
            self.ui.dark_curr_ref.setEnabled(True)
            log.debug("enabled")
