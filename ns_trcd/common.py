import numpy as np
from dataclasses import dataclass
from typing import Union


POINTS = 1_000

SHOULD_STOP = False


@dataclass
class PlotData:
    """Raw and processed data to be displayed in the UI.

    Notes
    -----
    The data in the da_* and avg_da_* fields are not always new since it takes
    two acquisitions to calculate those signals.
    """

    par: np.array
    perp: np.array
    ref: np.array
    da_par: Union[np.array, None]
    da_perp: Union[np.array, None]
    da_cd: Union[np.array, None]
    avg_da_par: Union[np.array, None]
    avg_da_perp: Union[np.array, None]
    avg_da_cd: Union[np.array, None]


@dataclass
class RawData:
    """Data from a single oscilloscope acquisition.
    """

    par: np.ndarray
    perp: np.ndarray
    ref: np.ndarray
    has_pump: bool


@dataclass
class Preamble:
    """Data needed to reconstruct oscilloscope signals from the raw data.
    """

    t_res: float
    v_scale_par: float
    v_offset_par: float
    v_scale_perp: float
    v_offset_perp: float
    v_scale_ref: float
    v_offset_ref: float
    points: int


@dataclass
class UiSettings:
    """Settings provided by the user via the UI.
    """
    start_pt: Union[int, None] = None
    stop_pt: Union[int, None] = None
    instr_name: Union[str, None] = None
    dark_curr_par: Union[float, None] = None
    dark_curr_perp: Union[float, None] = None
    dark_curr_ref: Union[float, None] = None
    num_measurements: int = 5
    save: bool = False
    save_loc: Union[str, None] = None
