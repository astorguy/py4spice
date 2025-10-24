"""Convert text file simulation results to objects"""

from pathlib import Path

import numpy as np
from matplotlib.ticker import EngFormatter

from .globals_types import TABLE_DATA, AnaType, numpy_flt


class SimResults:
    """Create objects for results extracted from simulation text files.
    Depending on the analysis type, the data is stored in different ways:
    either a plot or a table (dictionary).
    """

    def __init__(
        self,
        analysis_type: AnaType,
        header: list[str],
        data_plot: numpy_flt,
        data_table: dict[str, float],
    ):
        self.analysis_type: AnaType = analysis_type
        self.header: list[str] = header
        self.data_plot: numpy_flt = data_plot
        self.data_table: dict[str, float] = data_table

    def __str__(self) -> str:
        string = f"analysis_type: {self.analysis_type}\n\n"
        string += f"header:\n{self.header}\n\n"
        string += f"data_plot:\n{self.data_plot}"
        string += f"data_table:\n{self.data_table}"
        return string

    @staticmethod
    def _table_processing(filename: Path) -> dict[str, float]:
        """Process a text file with table data and return a dictionary"""
        data_dict: dict[str, float] = {}  # define empty dictionary
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:  # for each line: 1st word: key, last word: value
                words = line.split()
                data_dict[str(words[0])] = float(words[-1])
        return data_dict

    @staticmethod
    def _plot_processing(filename: Path) -> tuple[list[str], numpy_flt]:
        """Convert simulation text data that is in the form of a plot.

        Args:
            filename (Path): text file results from a simulation

        Returns:
            tuple[list[str], numpy_flt]: header and footer data
        """
        # turn first row into list of words for header
        with open(filename, "r", encoding="utf-8") as file:
            first_line = file.readline().strip()
            header = first_line.split()

        # skip the header and put data to 2d numpy
        data = np.genfromtxt(filename, dtype=float, skip_header=1)

        return header, data

    @staticmethod
    def _find_duplicate_indexes(strings: list[str]) -> list[int]:
        """determine which indices are duplicates

        Args:
            strings (list[str]): simulation text data in

        Returns:
            list[int]: simulation text data in
        """
        duplicate_indexes: list[int] = []
        seen: set[str] = set()

        for i, string in enumerate(strings):
            if string in seen:
                duplicate_indexes.append(i)
            else:
                seen.add(string)

        return duplicate_indexes

    @staticmethod
    def _mag_phase_convert(
        header_in: list[str], data_plot_in: numpy_flt
    ) -> tuple[list[str], numpy_flt]:
        """Convert real and imaginary data to magnitude and phase"""
        header_out = header_in.copy()
        data_plot_out = data_plot_in.copy()
        for i in range(len(header_out) - 1):
            current_name = header_out[i]
            next_name = header_out[i + 1]
            if current_name == next_name:
                real_part = data_plot_out[:, i]
                imag_part = data_plot_out[:, i + 1]
                # 1e-20 is added to avoid log(0) error
                mag = 20 * np.log10(np.sqrt(real_part**2 + imag_part**2) + 1e-20)
                phase = np.arctan2(imag_part, real_part) * 180 / np.pi
                data_plot_out[:, i] = mag
                data_plot_out[:, i + 1] = phase
                header_out[i] += "-mag"
                header_out[i + 1] += "-phase"
        return header_out, data_plot_out

    @staticmethod
    def _remove_dups(
        header_in: list[str], data_in: numpy_flt
    ) -> tuple[list[str], numpy_flt]:
        """remove duplicate columns before creating an object

        Args:
            header_in (list[str]): header info in text form
            data_in (numpy_flt): 2d numpy of data

        Returns:
            tuple[list[str], numpy_flt]: data ready to make object
        """
        dup_indexes: list[int] = SimResults._find_duplicate_indexes(header_in)

        # delete dups in data numpy array
        data_without_dups = np.delete(data_in, dup_indexes, axis=1)

        # delete dups from header
        for index in sorted(dup_indexes, reverse=True):
            del header_in[index]
        header_without_dups = header_in

        return header_without_dups, data_without_dups

    @classmethod
    def from_file(cls, analysis_type: AnaType, filename: Path) -> "SimResults":
        """Create a SimResults object from a text file. In other words,
        read in the simulation results file.
        """
        if analysis_type in TABLE_DATA:
            return cls(analysis_type, [], np.array([]), cls._table_processing(filename))

        # if not table data, then it is plot data
        (header1, data_plot1) = cls._plot_processing(filename)

        # if frequency analysis
        if analysis_type in ["ac", "noise"]:
            # convert to mag and phase
            (header2, data_plot2) = cls._mag_phase_convert(header1, data_plot1)
            # remove duplicate columns
            (header3, data_plot3) = cls._remove_dups(header2, data_plot2)
            return cls(analysis_type, header3, data_plot3, {})

        # if not frequency analysis, time or valtage x-axis
        (header2, data_plot2) = cls._remove_dups(header1, data_plot1)
        return cls(analysis_type, header2, data_plot2, {})

    def table_for_print(self) -> str:
        """Convert table data to a string for printing"""

        # set up engineering notation function
        engFormat: EngFormatter = EngFormatter(places=3, sep="")

        max_key_len = max(len(key) for key in self.data_table)
        result = ""
        for key, value in self.data_table.items():
            value_str: str = engFormat(value)  # use engineering notation
            is_negative = value < 0  # Adjust padding based on sign
            padding = max_key_len + (2 if not is_negative else 1)
            formatted_row = f"{key:<{padding}}{value_str}"
            result += formatted_row + "\n"
        return result