"""Signal measurements"""

from typing import Any

import numpy as np
from scipy.interpolate import interp1d

from .globals_types import numpy_flt


class StepInfo:
    """Measurements of a waveform step"""

    def __init__(
        self,
        x_array_in: numpy_flt,
        y_array_in: numpy_flt,
        xbegin: float,
        xend: float,
        npts: int,
    ) -> None:
        self.x_array_in = x_array_in
        self.y_array_in = y_array_in
        self.xbegin = xbegin
        self.xend = xend
        self.npts = npts
        self.thres_start = 0.01
        self.thres_lo = 0.1
        self.thres_hi = 0.9
        self.setting_err_percent = 0.02

    def f_y(self, x_values) -> Any:
        """Interpolate y value at a given x"""
        funct = interp1d(self.x_array_in, self.y_array_in, "linear")
        return funct(x_values)

    def y_at_x(self, x_value: float) -> float:
        """Return Y value for a X value"""
        return self.f_y(x_value)

    @property
    def x_array_lin(self) -> numpy_flt:
        """Linear-spaced points for x np.array"""
        return np.linspace(self.xbegin, self.xend, self.npts)

    @property
    def y_array_lin(self) -> numpy_flt:
        """Linear-spaced points for y array"""
        return self.f_y(self.x_array_lin)

    @property
    def yinit(self) -> float:
        """Y value at start of impulse"""
        return self.f_y(self.xbegin)

    @property
    def yfinal(self) -> float:
        """Y settle value"""
        return self.f_y(self.xend)

    @property
    def ydelta(self) -> float:
        """amount of step"""
        return self.yfinal - self.yinit

    @property
    def ylo(self) -> float:
        """Y at low part of rise"""
        return self.yinit + self.ydelta * self.thres_lo

    @property
    def ymid(self) -> float:
        """Y at 50% rise"""
        return self.yinit + self.ydelta * 0.5

    @property
    def yhi(self) -> float:
        """Y at at low part of rise"""
        return self.yinit + self.ydelta * self.thres_hi

    @property
    def xlo(self) -> float:
        """X when Y at rise low threshold"""
        idxs = np.where(self.y_array_lin >= self.ylo)[0]
        if idxs.size == 0:
            raise ValueError("No sample point meets the low threshold (ylo).")
        index = int(idxs[0])  # convert numpy index to Python int
        return float(self.x_array_lin[index])  # convert numpy scalar to builtin float

    @property
    def xmid(self) -> float:
        """X when Y at 50% rise"""
        idxs = np.where(self.y_array_lin >= self.ymid)[0]
        if idxs.size == 0:
            raise ValueError("No sample point meets the mid threshold (ymid).")
        index = int(idxs[0])  # convert numpy index to Python int
        return float(self.x_array_lin[index])  # convert numpy scalar to builtin float

    @property
    def xhi(self) -> float:
        """X when Y at rise hi threshold"""
        idxs = np.where(self.y_array_lin >= self.yhi)[0]
        if idxs.size == 0:
            raise ValueError("No sample point meets the high threshold (yhi).")
        index = int(idxs[0])  # convert numpy index to Python int
        return float(self.x_array_lin[index])  # convert numpy scalar to builtin float

    @property
    def risetime(self) -> float:
        """risetime"""
        return self.xhi - self.xlo

    @property
    def peak(self) -> float:
        """peak Y value"""
        index = np.argmax(self.y_array_lin)
        return self.y_array_lin[index]

    @property
    def peaktime(self) -> float:
        """X value at peak"""
        index = np.argmax(self.y_array_lin)
        return self.x_array_lin[index]

    @property
    def xinit(self) -> float:
        """X value where Y starts risings"""

        # thres where y approaches xbegin
        y_thres = self.yinit + self.ydelta * self.thres_start

        # array of indices where y <= y_thres
        y_less_equal_thres = np.where(self.y_array_lin <= y_thres)[0]

        if y_less_equal_thres.size == 0:
            # This should generally not happen if thres_start is small and the
            # data starts at yinit, but it handles the potential edge case.
            raise ValueError("No sample point is below the starting threshold (xinit).")

        index = y_less_equal_thres[-1]

        # Convert index to Python int and result to float for consistency
        return float(self.x_array_lin[int(index)])

    @property
    def settlingtime(self) -> float:
        """time it takes for y to stay within error range"""
        y_settle_err = self.ydelta * self.setting_err_percent
        y_err_lo = self.yfinal - y_settle_err
        y_err_hi = self.yfinal + y_settle_err

        indices_equal_less_err_lo = np.where(self.y_array_lin <= y_err_lo)[0]
        indices_equal_greater_err_hi = np.where(self.y_array_lin >= y_err_hi)[0]

        # Initialize last_index to the index of the last point (safe default)
        last_index = len(self.y_array_lin) - 1

        # Check if there are points below the low error threshold
        if len(indices_equal_less_err_lo) > 0:
            # If so, the last_index is the last time it dipped below
            last_index = indices_equal_less_err_lo[-1]

        # Check if there are points above the high error threshold
        if len(indices_equal_greater_err_hi) > 0:
            # If the last time it went above is later than the last time it went below, use that index
            if indices_equal_greater_err_hi[-1] > last_index:  # Use '>' not '>='
                last_index = indices_equal_greater_err_hi[-1]

        # Explicitly convert the index to a Python int to satisfy Pylance
        final_index_int = int(last_index)

        # Ensure the final calculation is returned as a float
        return float(self.x_array_lin[final_index_int] - self.xinit)
