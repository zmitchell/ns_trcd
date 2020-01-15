import numpy as np
from dataclasses import dataclass
from PySide2.QtWidgets import QMainWindow
from PySide2.QtCore import QThread, QObject, Signal, Slot, QTimer
from .generated_ui import Ui_MainWindow


@dataclass
class DataUpdate:
    time: np.ndarray
    par: np.ndarray
    perp: np.ndarray
    ref: np.ndarray
    par_da: np.ndarray
    perp_da: np.ndarray
    cd: np.ndarray
    new_da: bool


class ComputationSignals(QObject):
    """Signals produced by the computation worker

    exiting : no data
        Emitted when the worker is done with all computations and about to shut down.
    error : (exctype, value, traceback.format_exc())
        Emitted when the worker encounters and error.
    data : DataUpdate
        Emitted when new data is ready.
    """

    exiting = Signal()
    error = Signal(tuple)
    data = Signal(object)


class ComputationWorker(QObject):
    """Worker thread responsible for computing and storing experiment data.

    This worker receives the raw data from the perpendicular, parallel, and reference channels,
    then performs the dA and CD calculations on that data. The data is then stored and passed on
    to be displayed in the GUI.

    Notes
    -----
    Currently only generates dummy data via RNG.
    """

    def __init__(self):
        super(ComputationWorker, self).__init__()
        self.signals = ComputationSignals()
        self.rng = np.random.default_rng()
        self.counter = 1
        self.exiting = False
        self.timer = QTimer()
        self.timer.setInterval(10)  # in ms
        self.timer.timeout.connect(self.generate)
        self.timer.start()

    @Slot()
    def generate(self):
        """A temporary method that generates dummy data on each iteration of the timer.
        """
        POINTS = 1_000
        time = np.arange(POINTS)
        par = self.rng.random(POINTS)
        perp = self.rng.random(POINTS)
        ref = self.rng.random(POINTS)
        par_da = self.rng.random(POINTS)
        perp_da = self.rng.random(POINTS)
        cd = self.rng.random(POINTS)
        data = DataUpdate(
            time, par, perp, ref, par_da, perp_da, cd, self.counter % 2 == 0
        )
        self.counter += 1
        self.signals.data.emit(data)

    def finish(self):
        """A temporary method used to stop the timer that triggers data generation.
        """
        self.timer.stop()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.start_btn.clicked.connect(self.start_collection)
        self.ui.stop_btn.clicked.connect(self.stop_collection)
        self.collecting = False
        self.comp_thread = QThread()
        self.live_par_line = self.ui.live_par_graph.plot(np.arange(100), np.zeros(100))
        self.live_perp_line = self.ui.live_perp_graph.plot(
            np.arange(100), np.zeros(100)
        )
        self.live_ref_line = self.ui.live_ref_graph.plot(np.arange(100), np.zeros(100))
        self.live_par_da_line = self.ui.live_par_da_graph.plot(
            np.arange(100), np.zeros(100)
        )
        self.live_perp_da_line = self.ui.live_perp_da_graph.plot(
            np.arange(100), np.zeros(100)
        )
        self.live_cd_line = self.ui.live_cd_graph.plot(np.arange(100), np.zeros(100))

    @Slot()
    def start_collection(self):
        """Begins generating data when the "Start" button is pressed.
        """
        if self.collecting:
            return
        self.comp_worker = ComputationWorker()
        self.comp_worker.signals.data.connect(self.update_plots)
        self.comp_worker.moveToThread(self.comp_thread)
        self.comp_thread.start()
        self.collecting = True

    @Slot()
    def stop_collection(self):
        """Stops generating data when the "Stop" button is pressed.
        """
        if not self.collecting:
            return
        self.comp_worker.finish()
        self.comp_thread.quit()
        self.comp_thread.wait()
        self.collecting = False

    @Slot(object)
    def update_plots(self, new_data):
        """Update the plots in the "Live" tab when new data is available.
        """
        self.live_par_line.setData(new_data.time, new_data.par)
        self.live_perp_line.setData(new_data.time, new_data.perp)
        self.live_ref_line.setData(new_data.time, new_data.ref)
        if new_data.new_da:
            self.live_par_da_line.setData(new_data.time, new_data.par_da)
            self.live_perp_da_line.setData(new_data.time, new_data.perp_da)
            self.live_cd_line.setData(new_data.time, new_data.cd)
