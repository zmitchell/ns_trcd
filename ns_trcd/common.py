import numpy as np
from dataclasses import dataclass


POINTS = 1_000


@dataclass
class PlotData:
    """Raw and processed data to be displayed in the UI.

    Notes
    -----
    The data in the da_* and avg_da_* fields are not always new since it takes
    two acquisitions to calculate those signals.
    """

    time: np.ndarray
    par: np.ndarray
    perp: np.ndarray
    ref: np.ndarray
    da_par: np.ndarray
    da_perp: np.ndarray
    da_cd: np.ndarray
    avg_da_par: np.ndarray
    avg_da_perp: np.ndarray
    avg_da_cd: np.ndarray
    new_da: bool


@dataclass
class RawData:
    """Data from a single oscilloscope acquisition.
    """

    par: np.ndarray
    perp: np.ndarray
    ref: np.ndarray
    shutter: np.ndarray
