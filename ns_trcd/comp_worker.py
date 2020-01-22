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
        self.signals = ComputationSignals()
        self.exiting = False
        self.count = 0
        self.max_measurements = num_measurements
        self.avg_da_par = np.zeros(POINTS)
        self.avg_da_perp = np.zeros(POINTS)
        self.avg_da_cd = np.zeros(POINTS)
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
        self.v_offset_shutter = preamble.v_offset_shutter
        self.v_scale_par = preamble.v_scale_par
        self.v_scale_perp = preamble.v_scale_perp
        self.v_scale_ref = preamble.v_scale_ref
        self.v_scale_shutter = preamble.v_scale_shutter
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
        print("comp: begin")
        par = data.par * self.v_scale_par + self.v_offset_par
        perp = data.perp * self.v_scale_perp + self.v_offset_perp
        ref = data.ref * self.v_scale_ref + self.v_offset_ref
        shutter = data.shutter * self.v_scale_shutter + self.v_offset_shutter
        has_pump = np.mean(shutter) > 2.5
        print(f"comp: shutter mean: {np.mean(shutter)}")
        print(f"comp: has pump: {has_pump}")
        # If we got a "with pump" curve when we already had one (or vice versa), then
        # something went wrong and we got out of sequence. Clear what data we already
        # had stored, and store the most current data.
        if has_pump and (self.with_pump is not None):
            print("comp: replacing with_pump")
            self.with_pump = MeasurementData(par, perp, ref)
            self.without_pump = None
        elif has_pump:
            print("comp: storing with_pump")
            self.with_pump = MeasurementData(par, perp, ref)
        if (not has_pump) and (self.without_pump is not None):
            print("comp: replacing without_pump")
            self.without_pump = MeasurementData(par, perp, ref)
            self.with_pump = None
        elif (not has_pump):
            print("comp: storing without_pump")
            self.without_pump = MeasurementData(par, perp, ref)
        # Compute the dA signals if we have both required sets of data
        if (self.with_pump is not None) and (self.without_pump is not None):
            self.count += 1
            print(f"comp: count={self.count}")
            da_par = -np.log10(
                np.divide(
                    np.divide(self.with_pump.par, self.with_pump.ref),
                    np.divide(self.without_pump.par, self.without_pump.ref)))
            da_perp = -np.log10(
                np.divide(
                    np.divide(self.with_pump.perp, self.with_pump.ref),
                    np.divide(self.without_pump.perp, self.without_pump.ref)))
            da_cd = (4 / 2.3) * (np.divide(self.with_pump.perp, self.with_pump.par) - np.divide(self.without_pump.perp, self.without_pump.par))
            if self.count == 1:
                self.avg_da_par = da_par
                self.avg_da_perp = da_perp
                self.avg_da_cd = da_cd
            else:
                self.avg_da_par = (self.count - 1) / (self.count) * self.avg_da_par + 1 / self.count * da_par
                self.avg_da_perp = (self.count - 1) / (self.count) * self.avg_da_perp + 1 / self.count * da_perp
                self.avg_da_cd = (self.count - 1) / (self.count) * self.avg_da_cd + 1 / self.count * da_cd
            plot_data = PlotData(
                par,
                perp,
                ref,
                da_par,
                da_perp,
                da_cd,
                self.avg_da_par,
                self.avg_da_perp,
                self.avg_da_cd)
            print(da_par)
            self.signals.new_data.emit(plot_data)
            self.with_pump = None
            self.without_pump = None
            if self.count >= self.max_measurements:
                self.mutex.lock()
                common.SHOULD_STOP = True
                self.mutex.unlock()
        else:
            plot_data = PlotData(
                par,
                perp,
                ref,
                None,
                None,
                None,
                None,
                None,
                None)
            self.signals.new_data.emit(plot_data)
            # self.with_pump = None
            # self.without_pump = None
