import numpy as np
from PySide2.QtCore import QObject, Signal, Slot
from .common import PlotData, RawData, POINTS


class ComputationSignals(QObject):
    """Signals produced by the computation worker

    data : PlotData
        Emitted when new data is ready.
    """

    new_data = Signal(PlotData)


class ComputationWorker(QObject):
    """Worker thread responsible for computing and storing experiment data.

    This worker receives the raw data from the perpendicular, parallel, and reference
    channels, then performs the dA and CD calculations on that data. The data is then
    stored and passed on to be displayed in the GUI.

    Notes
    -----
    Currently only performs dummy calculations with dummy data sent from the experiment
    worker.
    """

    def __init__(self):
        super(ComputationWorker, self).__init__()
        self.signals = ComputationSignals()
        self.exiting = False
        self.count = 0
        self.avg_da_par = np.zeros(POINTS)
        self.avg_da_perp = np.zeros(POINTS)
        self.avg_da_cd = np.zeros(POINTS)

    @Slot(RawData)
    def compute_signals(self, data):
        """Compute dA from the oscilloscope traces.

        Parameters
        ----------
        data : RawData
            The parallel, perpendicular, reference, and shutter traces from
            the oscilloscope.

        Emits
        -----
        PlotData

        Notes
        -----
        New dA traces are only generated on every other acquisition since you
        need measurements with and without the pump in order to calculate dA.
        """

        time = np.arange(POINTS)
        da_par = data.par + data.ref
        da_perp = data.perp + data.ref
        da_cd = data.par + data.perp
        self.count += 1
        if (self.count >= 2) and (self.count % 2 == 0):
            if self.count == 2:  # the first round, nothing to average yet
                self.avg_da_par = da_par
                self.avg_da_perp = da_perp
                self.avg_da_cd = da_cd
            else:
                self.avg_da_par = (self.count - 1) / self.count * self.avg_da_par + (
                    1 / self.count
                ) * da_par
                self.avg_da_perp = (self.count - 1) / self.count * self.avg_da_perp + (
                    1 / self.count
                ) * da_perp
                self.avg_da_cd = (self.count - 1) / self.count * self.avg_da_cd + (
                    1 / self.count
                ) * da_cd
        data = PlotData(
            time,
            data.par,
            data.perp,
            data.ref,
            da_par,
            da_perp,
            da_cd,
            self.avg_da_par,
            self.avg_da_perp,
            self.avg_da_cd,
            self.count % 2 == 0,
        )
        self.signals.new_data.emit(data)
