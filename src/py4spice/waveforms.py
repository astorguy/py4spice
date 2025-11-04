from typing import TypeAlias

import numpy as np
import numpy.typing as npt
from scipy.interpolate import interp1d

numpy_flt: TypeAlias = npt.NDArray[np.float64]


class Waveforms:
    """Waveforms with a single x value and one or more y values in a 2D numpy array.
    header defines the column names."""

    def __init__(self, header: list[str], data: numpy_flt, npts: int = 1000):
        self.header: list[str] = header

        column_count: int = data.shape[1]  # number of columns
        self.data: numpy_flt = np.zeros((npts, column_count))
        self.data[:, 0] = np.linspace(data[0, 0], data[-1, 0], npts)

        # interpolate y-values for each column
        x: numpy_flt = data[:, 0]
        for i in range(1, column_count):
            y: numpy_flt = data[:, i]
            f = interp1d(x, y)
            self.data[:, i] = f(self.data[:, 0])

    @property
    def npts(self) -> int:
        """number of data points (rows) in the waveform"""
        return int(self.data.shape[0])

    def vec_subset(self, vecs: list[str]) -> None:
        """create a smaller subset of the header vectors

        Args:
            vecs (list[str]): vector subset
        """
        if set(vecs).issubset(self.header):
            indices_for_deletion = [
                index for index, item in enumerate(self.header) if item not in vecs
            ]
            indices_for_deletion.sort(reverse=True)
            del indices_for_deletion[-1]  # remove index 0 (x-axis) from list

            # Delete header names & data columns, starting from end, working backwards
            for i in indices_for_deletion:
                del self.header[i]
                self.data = np.delete(self.data, i, axis=1)
        else:
            print("Error: vecs is not a subset of the header list")

    def x_range(self, x_begin: float, x_end: float, npts: int = 1000) -> None:
        """Limit range of data and create linear-spaced points

        Args:
            x_begin (float): new x start
            x_end (float): new x end
            npts (int): number of linear points in new array
        """
        x_orig = self.data[:, 0]
        y_origs = self.data[:, 1:]
        x_new = np.linspace(x_begin, x_end, npts)
        new_array = np.zeros((npts, y_origs.shape[1] + 1))
        new_array[:, 0] = x_new

        # Interpolate y columns using interp1d
        for i in range(y_origs.shape[1]):
            funct = interp1d(x_orig, y_origs[:, i])
            new_array[:, i + 1] = funct(x_new)

        self.data = new_array

    def single_column(self, signal_name: str) -> numpy_flt:
        """Returns a single Numpy Array for the wave"""
        index: int = self.header.index(signal_name)
        return self.data[:, index]

    def x_axis_and_sigs(self, signal_names: list[str]) -> list[numpy_flt]:
        """Returns X-Axis numpy and all the waves"""

        list_of_numpys = [self.data[:, 0]]  # First, the x-axis (always 1st col.)
        for signal_name in signal_names:
            list_of_numpys.append(self.single_column(signal_name))

        return list_of_numpys

    def new_wave(self, wave_name: str, column: numpy_flt) -> None:
        """Add a new waveform to the object"""
        self.header.append(wave_name)
        self.data = np.column_stack((self.data, column))

    def multiply(self, factor1_name: str, factor2_name: str, result_name: str) -> None:
        """Multiply two waves and store in a new wave"""
        factor1 = self.single_column(factor1_name)
        factor2 = self.single_column(factor2_name)
        result = np.multiply(factor1, factor2)
        self.new_wave(result_name, result)

    def scaler(self, factor: float, wave_name: str, result_name: str) -> None:
        """Multiply a wave by a scalar and store in a new wave"""
        wave = self.single_column(wave_name)
        self.new_wave(result_name, factor * wave)

    def divide(self, dividend_name: str, divisor_name: str, result_name: str) -> None:
        """Divide two waves and store in a new wave"""
        dividend = self.single_column(dividend_name)
        divisor = self.single_column(divisor_name)

        # Use numpy's divide function to handle division by zero
        result = np.divide(
            dividend, divisor, out=np.zeros_like(dividend), where=divisor != 0
        )

        self.new_wave(result_name, result)
