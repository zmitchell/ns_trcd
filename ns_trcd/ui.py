import numpy as np
from PySide2.QtWidgets import QMainWindow
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
        self.ui.start_btn.clicked.connect(self.start_collecting)
        self.ui.stop_btn.clicked.connect(self.stop_collecting)
        self.collecting = False
        self.comp_thread = QThread()
        self.exp_thread = QThread()
        self._store_line_objects()
        self.time_axis = None

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

    @Slot(np.ndarray)
    def set_time_axis(self, values):
        self.time_axis = values

    @Slot()
    def start_collecting(self):
        """Begins generating data when the "Start" button is pressed.
        """
        if self.collecting:
            return
        common.SHOULD_STOP = False
        self.mutex = QMutex()
        self.comp_worker = ComputationWorker(self.mutex, self.ui.measurements.value())
        self.exp_worker = ExperimentWorker(self.mutex, self.ui.instr_name.text())
        self.exp_worker.signals.preamble.connect(self.comp_worker.store_preamble)
        self.exp_worker.signals.new_data.connect(self.comp_worker.compute_signals)
        self.exp_worker.signals.done.connect(self.cleanup_when_done)
        self.comp_worker.signals.time_axis.connect(self.set_time_axis)
        self.comp_worker.signals.new_data.connect(self.update_plots)
        self.signals.measure.connect(self.exp_worker.measure)
        self.comp_worker.moveToThread(self.comp_thread)
        self.exp_worker.moveToThread(self.exp_thread)
        self.comp_thread.start()
        self.exp_thread.start()
        self.signals.measure.emit()
        self.collecting = True

    @Slot()
    def stop_collecting(self):
        """Stops generating data when the "Stop" button is pressed.
        """
        if not self.collecting:
            return
        self.mutex.lock()
        common.SHOULD_STOP = True
        self.mutex.unlock()
        self.comp_thread.quit()
        self.exp_thread.quit()
        self.comp_thread.wait()
        self.exp_thread.wait()
        self.collecting = False

    @Slot()
    def cleanup_when_done(self):
        """
        """
        self.comp_thread.quit()
        self.exp_thread.quit()
        self.comp_thread.wait()
        self.exp_thread.wait()
        self.collecting = False
        self.mutex.lock()
        common.SHOULD_STOP = False
        self.mutex.unlock()

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
