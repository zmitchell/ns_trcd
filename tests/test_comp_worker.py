import numpy as np
from ns_trcd.comp_worker import ComputationWorker, MeasurementData, ComputationSignals
from ns_trcd.common import UiSettings, Preamble, RawData
from ns_trcd import common
from PySide2.QtCore import QMutex
from pytest import fixture


@fixture
def empty_settings() -> UiSettings:
    """Return a UiSettings with all default values.
    """
    return UiSettings()


@fixture
def empty_worker(empty_settings) -> ComputationWorker:
    mutex = QMutex()
    return ComputationWorker(mutex, empty_settings)


@fixture
def preamble() -> Preamble:
    """Returns a preamble filled with dummy values.
    """
    return Preamble(
        t_res=20e-9,
        v_scale_par=1.0,
        v_offset_par=0,
        v_scale_perp=1.0,
        v_offset_perp=0,
        v_scale_ref=1.0,
        v_offset_ref=0,
        points=1000)


@fixture
def preambled_worker(empty_worker, preamble) -> ComputationWorker:
    empty_worker.store_preamble(preamble)
    return empty_worker


@fixture
def measurement_data() -> MeasurementData:
    par = np.full(100, 1.0)
    perp = np.full(100, 1.0)
    ref = np.full(100, 1.0)
    return MeasurementData(par, perp, ref)


@fixture
def raw_data_with_pump() -> RawData:
    return RawData(
        par=np.full(100, 1.0),
        perp=np.full(100, 1.0),
        ref=np.full(100, 1.0),
        has_pump=True)


@fixture
def raw_data_without_pump() -> RawData:
    return RawData(
        par=np.full(100, 1.0),
        perp=np.full(100, 1.0),
        ref=np.full(100, 1.0),
        has_pump=False)


def test_can_create_comp_worker(empty_settings):
    mutex = QMutex()
    ComputationWorker(mutex, empty_settings)


def test_stores_preamble(empty_worker, preamble):
    assert empty_worker.t_res is None
    assert empty_worker.v_scale_par is None
    assert empty_worker.v_offset_par is None
    assert empty_worker.v_scale_perp is None
    assert empty_worker.v_offset_perp is None
    assert empty_worker.v_scale_ref is None
    assert empty_worker.v_offset_ref is None
    assert empty_worker.points is None
    empty_worker.store_preamble(preamble)
    assert empty_worker.t_res == preamble.t_res
    assert empty_worker.v_scale_par == preamble.v_scale_par
    assert empty_worker.v_offset_par == preamble.v_offset_par
    assert empty_worker.v_scale_perp == preamble.v_scale_perp
    assert empty_worker.v_offset_perp == preamble.v_offset_perp
    assert empty_worker.v_scale_ref == preamble.v_scale_ref
    assert empty_worker.v_offset_ref == preamble.v_offset_ref
    assert empty_worker.points == preamble.points


def test_emits_time_axis_signal(qtbot, empty_worker, preamble):
    """Ensure that the worker emits the time_axis signal when the preamble is set.
    """
    with qtbot.waitSignal(empty_worker.signals.time_axis, timeout=1000):
        empty_worker.store_preamble(preamble)


def test_stores_without_pump_data(preambled_worker, raw_data_without_pump):
    preambled_worker.compute_signals(raw_data_without_pump)
    assert preambled_worker.without_pump is not None
    assert preambled_worker.with_pump is None


def test_stores_with_pump_data(preambled_worker, raw_data_with_pump):
    preambled_worker.compute_signals(raw_data_with_pump)
    assert preambled_worker.with_pump is not None
    assert preambled_worker.without_pump is None


def test_dark_current_compensated(empty_settings, preamble, raw_data_without_pump):
    """Ensure that dark current is subtracted from the raw signals.

    The dummy preamble is populated with signals around 1.0, so we subtract
    a dark current of 0.5 in order to be able to very clearl distinguish
    when the dark current has been subtracted.
    """
    settings = empty_settings
    settings.dark_curr_par = 0.5
    mutex = QMutex()
    worker = ComputationWorker(mutex, settings)
    worker.store_preamble(preamble)
    worker.compute_signals(raw_data_without_pump)
    assert worker.without_pump.par.mean() < 0.75


def test_ignores_double_pump(preambled_worker, raw_data_with_pump):
    """Ensure that two "with pump"s in a row don't trigger a dA calculation.
    """
    initial_count = preambled_worker.count
    first_raw_data = raw_data_with_pump
    second_raw_data = raw_data_with_pump
    # add something to be able to tell the difference between the two different
    # sets of data once they're stored.
    second_raw_data.par += 1.0
    preambled_worker.compute_signals(first_raw_data)
    preambled_worker.compute_signals(second_raw_data)
    assert preambled_worker.without_pump is None
    par_mean = preambled_worker.with_pump.par.mean()
    assert par_mean < 2.01
    assert par_mean > 1.99
    assert preambled_worker.count == initial_count


def test_ignores_double_no_pump(preambled_worker, raw_data_without_pump):
    """Ensure that two "without pump"s in a row don't trigger a dA calculation.
    """
    initial_count = preambled_worker.count
    first_raw_data = raw_data_without_pump
    second_raw_data = raw_data_without_pump
    # add something to be able to tell the difference between the two different
    # sets of data once they're stored.
    second_raw_data.par += 1.0
    preambled_worker.compute_signals(first_raw_data)
    preambled_worker.compute_signals(second_raw_data)
    assert preambled_worker.with_pump is None
    par_mean = preambled_worker.without_pump.par.mean()
    assert par_mean < 2.01
    assert par_mean > 1.99
    assert preambled_worker.count == initial_count


def test_increases_count(preambled_worker, raw_data_without_pump, raw_data_with_pump):
    """Ensure that the measurement count increases with a full set of data.
    """
    initial_count = preambled_worker.count
    preambled_worker.compute_signals(raw_data_with_pump)
    preambled_worker.compute_signals(raw_data_without_pump)
    assert preambled_worker.count == (initial_count + 1)


def test_new_data_signal_emitted(qtbot, preambled_worker, raw_data_without_pump):
    """Ensure that the new_data signal is emitted when signals are computed.
    """
    with qtbot.waitSignal(preambled_worker.signals.new_data, timeout=1000):
        preambled_worker.compute_signals(raw_data_without_pump)


def test_clears_data_after_computing_da(preambled_worker, raw_data_without_pump, raw_data_with_pump):
    """Ensure that old data doesn't stick around after computing dA.
    """
    assert preambled_worker.with_pump is None
    assert preambled_worker.without_pump is None
    preambled_worker.compute_signals(raw_data_with_pump)
    preambled_worker.compute_signals(raw_data_without_pump)
    assert preambled_worker.with_pump is None
    assert preambled_worker.without_pump is None


def test_sets_should_stop_when_done(preambled_worker, raw_data_with_pump, raw_data_without_pump):
    assert not common.SHOULD_STOP
    preambled_worker.max_measurements = 1
    preambled_worker.compute_signals(raw_data_with_pump)
    preambled_worker.compute_signals(raw_data_without_pump)
    assert common.SHOULD_STOP
    common.SHOULD_STOP = False
