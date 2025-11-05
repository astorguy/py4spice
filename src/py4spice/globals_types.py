"""Global constants and types"""

from typing import TypeAlias, Literal
import numpy as np
import numpy.typing as npt

# Alias for type checking
numpy_flt: TypeAlias = npt.NDArray[np.float64]

AnaType: TypeAlias = Literal[
    "ac", "dc", "disto", "noise", "op", "pz", "sens", "sp", "tf", "tran"
]

# Categorize so we can hanlde results correctly
TABLE_DATA: list[AnaType] = ["op", "sens", "tf"]
PLOT_DATA: list[AnaType] = ["ac", "dc", "disto", "noise", "pz", "sp", "tran"]
TIME_AXIS: list[AnaType] = ["tran"]
SIG_AXIS: list[AnaType] = ["dc"]
FREQ_AXIS: list[AnaType] = ["ac", "noise"]