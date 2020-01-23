import numpy as np
from dataclasses import dataclass
from PySide2.QtCore import QObject, Signal, Slot
from . import common
from .common import PlotData, RawData, Preamble, POINTS


@dataclass
class MeasurementData:
    par: np.array
    perp: np.array
    ref: np.array


class ComputationSignals(QObject):
    """Signals produced by the computation worker

    data : PlotData
        Emitted when new data is ready.
    stop_measuring : empty
        Emitted when the last measurement has been collected
    """

    new_data = Signal(PlotData)
    time_axis = Signal(np.ndarray)
    meas_num = Signal(int)
    stop_measuring = Signal()


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

    def __init__(self, mutex, num_measurements):
        super(ComputationWorker, self).__init__()
        self.mutex = mutex
        self.signals = ComputationSignals()
        self.exiting = False
        self.count = 0
        self.max_measurements = num_measurements
        self.avg_da_par = np.zeros(POINTS)
        self.avg_da_perp = np.zeros(POINTS)
        self.avg_da_cd = np.zeros(POINTS)
        self.should_reset_averages = False
        self.average_count = 0
        self.with_pump = None
        self.without_pump = None
        self.t_res = None
        self.v_offset_par = None
        self.v_offset_perp = None
        self.v_offset_ref = None
        self.v_offset_shutter = None
        self.v_scale_par = None
        self.v_scale_perp = None
        self.v_scale_ref = None
        self.v_scale_shutter = None

    @Slot(Preamble)
    def store_preamble(self, preamble):
        """Store data needed to reconstruct oscilloscope traces.

        Parameters
        ----------
        preamble : Preamble
            Contains the time resolution, vertical offset, and vertical scale factor
            needed to construct a time axis and an oscilloscope trace.
        """
        self.t_res = preamble.t_res
        self.v_offset_par = preamble.v_offset_par
        self.v_offset_perp = preamble.v_offset_perp
        self.v_offset_ref = preamble.v_offset_ref
        self.v_scale_par = preamble.v_scale_par
        self.v_scale_perp = preamble.v_scale_perp
        self.v_scale_ref = preamble.v_scale_ref
        self.points = preamble.points
        time_values = self.t_res * np.arange(self.points)
        self.signals.time_axis.emit(time_values)

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
        par = data.par * self.v_scale_par + self.v_offset_par
        perp = data.perp * self.v_scale_perp + self.v_offset_perp
        ref = data.ref * self.v_scale_ref + self.v_offset_ref
        if data.has_pump:
            self.with_pump = MeasurementData(par, perp, ref)
        else:
            self.without_pump = MeasurementData(par, perp, ref)
        # Compute the dA signals if we have both required sets of data
        if (self.with_pump is not None) and (self.without_pump is not None):
            self.count += 1
            self.average_count += 1
            self.signals.meas_num.emit(self.count)
            da_par, da_perp, da_cd = self.compute_da()
            self.update_averages(da_par, da_perp, da_cd)
            plot_data = PlotData(
                par,
                perp,
                ref,
                da_par,
                da_perp,
                da_cd,
                self.avg_da_par,
                self.avg_da_perp,
                self.avg_da_cd,
            )
            self.signals.new_data.emit(plot_data)
            self.with_pump = None
            self.without_pump = None
            if self.count >= self.max_measurements:
                self.mutex.lock()
                common.SHOULD_STOP = True
                self.mutex.unlock()
        else:
            plot_data = PlotData(par, perp, ref, None, None, None, None, None, None)
            self.signals.new_data.emit(plot_data)

    def compute_da(self):
        da_par = -np.log10(
            np.divide(
                np.divide(self.with_pump.par, self.with_pump.ref),
                np.divide(self.without_pump.par, self.without_pump.ref),
            )
        )
        da_perp = -np.log10(
            np.divide(
                np.divide(self.with_pump.perp, self.with_pump.ref),
                np.divide(self.without_pump.perp, self.without_pump.ref),
            )
        )
        da_cd = (4 / 2.3) * (
            np.divide(self.with_pump.perp, self.with_pump.par)
            - np.divide(self.without_pump.perp, self.without_pump.par)
        )
        return da_par, da_perp, da_cd

    def update_averages(self, par, perp, cd):
        if self.count == 1:
            self.avg_da_par = par
            self.avg_da_perp = perp
            self.avg_da_cd = cd
        elif self.should_reset_averages:
            self.avg_da_par = par
            self.avg_da_perp = perp
            self.avg_da_cd = cd
            self.average_count = 1
            self.should_reset_averages = False
        else:
            self.avg_da_par = (self.average_count - 1) / (
                self.average_count
            ) * self.avg_da_par + 1 / self.average_count * par
            self.avg_da_perp = (self.average_count - 1) / (
                self.average_count
            ) * self.avg_da_perp + 1 / self.average_count * perp
            self.avg_da_cd = (self.average_count - 1) / (
                self.average_count
            ) * self.avg_da_cd + 1 / self.average_count * cd

    @Slot()
    def reset_averages(self):
        self.should_reset_averages = True
