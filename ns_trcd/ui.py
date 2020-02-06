import numpy as np
from pathlib import Path
from pyqtgraph import ViewBox
from PySide2.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PySide2.QtCore import QObject, QThread, Signal, Slot, QMutex
from . import common
from .common import PlotData
from .comp_worker import ComputationWorker
from .exp_worker import ExperimentWorker
from .generated_ui import Ui_MainWindow


class MainWindowSignals(QObject):
    measure = Signal()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.signals = MainWindowSignals()
        self.save_data_dir = None
        self.current_measurement = 0
        self.max_measurements = 0
        self.collecting = False
        self.time_axis = None
        self.mutex = QMutex()
        self.comp_thread = QThread()
        self.exp_thread = QThread()
        self._connect_components()
        self._set_initial_widget_states()
        self._store_line_objects()
        self._set_plot_mouse_mode()

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
        self.ui.stop_pt_checkbox.stateChanged.connect(self.stop_pt_set_state)

    def closeEvent(self, event):
        """Clean up worker threads if the window is closed while collecting data.

        Notes
        -----
        This overrides the default closeEvent method of QMainWindow.
        """
        if self.collecting:
            self.comp_thread.quit()
            self.exp_thread.quit()
            self.comp_thread.wait()
            self.exp_thread.wait()
        event.accept()

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
        self.time_axis = values

    @Slot(int)
    def update_max_measurements(self, x):
        self.max_measurements = x
        self.ui.measurement_counter_label.setText(
            f"{self.current_measurement}/{self.max_measurements}"
        )

    @Slot(int)
    def update_current_measurement(self, x):
        self.current_measurement = x
        self.ui.measurement_counter_label.setText(
            f"{self.current_measurement}/{self.max_measurements}"
        )

    @Slot()
    def start_collecting(self):
        """Begins collecting data when the "Start" button is pressed.
        """
        should_save = self.ui.save_data_checkbox.isChecked()
        if should_save and not self._saving_should_proceed():
            return
        common.SHOULD_STOP = False
        if should_save:
            self.comp_worker = ComputationWorker(
                self.mutex,
                self.ui.measurements.value(),
                save=True,
                save_dir=self.save_data_dir,
            )
        else:
            self.comp_worker = ComputationWorker(
                self.mutex, self.ui.measurements.value(), save=False
            )
        start_pt = self.ui.start_pt.value()
        if self.ui.stop_pt_checkbox.isChecked():
            self.exp_worker = ExperimentWorker(
                self.mutex, self.ui.instr_name.text(), start_pt=start_pt
            )
        else:
            stop_pt = self.ui.stop_pt.value()
            if start_pt >= stop_pt:
                self._tell_start_greater_than_stop()
                return
            self.exp_worker = ExperimentWorker(
                self.mutex,
                self.ui.instr_name.text(),
                start_pt=start_pt,
                stop_pt=stop_pt,
            )
        self._connect_worker_signals()
        self.comp_worker.moveToThread(self.comp_thread)
        self.exp_worker.moveToThread(self.exp_thread)
        self.comp_thread.start()
        self.exp_thread.start()
        self.signals.measure.emit()
        self._disable_acq_controls()

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
        self.mutex.lock()
        common.SHOULD_STOP = True
        self.mutex.unlock()
        self.comp_thread.quit()
        self.exp_thread.quit()
        self.comp_thread.wait()
        self.exp_thread.wait()
        self._enable_acq_controls()
        self.current_measurement = 0

    @Slot()
    def cleanup_when_done(self):
        """Clean up workers and threads after data collection is complete.
        """
        self.comp_thread.quit()
        self.exp_thread.quit()
        self.comp_thread.wait()
        self.exp_thread.wait()
        self.mutex.lock()
        common.SHOULD_STOP = False
        self.mutex.unlock()
        self._enable_acq_controls()
        self.current_measurement = 0
        QMessageBox.information(
            self, "Done", "The experiment has finished.", QMessageBox.StandardButton.Ok
        )

    @Slot(PlotData)
    def update_plots(self, data):
        """Update the plots in the Live/Average tabs when new data is available.

        Parameters
        ----------
        data : PlotData
            Three live data channels and the signals computed from them.
        """
        self.live_par_line.setData(self.time_axis, data.par)
        self.live_perp_line.setData(self.time_axis, data.perp)
        self.live_ref_line.setData(self.time_axis, data.ref)
        if data.da_par is not None:
            self.live_da_par_line.setData(self.time_axis, data.da_par)
            self.live_da_perp_line.setData(self.time_axis, data.da_perp)
            self.live_da_cd_line.setData(self.time_axis, data.da_cd)
            self.avg_da_par_line.setData(self.time_axis, data.avg_da_par)
            self.avg_da_perp_line.setData(self.time_axis, data.avg_da_perp)
            self.avg_da_cd_line.setData(self.time_axis, data.avg_da_cd)

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
        if state == 0:
            self.ui.save_loc.setDisabled(True)
            self.ui.save_loc_browse_btn.setDisabled(True)
        elif state == 2:
            self.ui.save_loc.setEnabled(True)
            self.ui.save_loc_browse_btn.setEnabled(True)

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
        try:
            loc_is_valid = self._save_loc_still_valid()
        except TypeError:
            loc_is_valid = False
        if not loc_is_valid:
            self._tell_save_loc_is_invalid()
            return False
        would_overwrite = self._save_would_overwrite()
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
        if state == 2:
            self.ui.stop_pt.setDisabled(True)
        elif state == 0:
            self.ui.stop_pt.setEnabled(True)

    def _tell_start_greater_than_stop(self):
        """Tell the user that the current save location isn't valid or doesn't exist.
        """
        QMessageBox.critical(
            self,
            "Invalid Start/Stop Points",
            "The Start point must be less than the Stop point.",
            QMessageBox.StandardButton.Ok,
        )
