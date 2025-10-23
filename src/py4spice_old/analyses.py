"""Vector set of signals for which to gather data, plot, ... """

from pathlib import Path
from typing import Literal
from .vectors import Vectors

AnalysisType = Literal["op", "dc", "tr", "ac"]  # typing for Analysis types


class Analyses:
    """Vector set of signals for which to gather data, plot, ..."""

    def __init__(
        self,
        name: str,
        cmd_type: AnalysisType,
        cmd: list[str | int | float],
        vector: Vectors,
        results_loc: Path,
    ) -> None:

        self.name: str = name
        self.cmd_type = cmd_type  # "tran", "ac", ...
        self.cmd_strings: list[str] = [str(item) for item in cmd]
        self.cmd_line: str = " ".join(self.cmd_strings)
        results_filename: Path = results_loc / f"{self.name}.txt"

        self.vec_output = ""  # initialize to nothing
        if self.cmd_type == "ac":
            self.vec_output = f"wrdata {results_filename} {vector}"
        if self.cmd_type == "dc":
            self.vec_output = f"wrdata {results_filename} {vector}"
        if self.cmd_type == "op":
            self.vec_output = f"print line {vector} > {results_filename}"
        if self.cmd_type == "tr":
            self.vec_output = f"wrdata {results_filename} {vector}"

    def lines_for_cntl(self) -> list[str]:
        """returns a list of the command lines for the control file

        Returns:
            list[str]: command lines
        """
        return [self.cmd_line, self.vec_output]
