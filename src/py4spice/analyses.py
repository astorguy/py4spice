from pathlib import Path

from .globals_types import AnaType
from .vectors import Vectors


class Analyses:
    """Prepares analysis command that will go into control file and be executed during simulation"""

    def __init__(
        self,
        name: str,
        cmd_type: AnaType,
        cmd: str,
        vector: Vectors,
        results_loc: Path,
    ) -> None:
        self.name = name
        self.cmd_type: AnaType = cmd_type  # "tran", "ac", ...
        self.cmd = cmd
        self.vector = vector
        self.results_loc = results_loc

    @property
    def results_filename(self) -> Path:
        """full path to the result file"""
        return self.results_loc / f"{self.name}.txt"

    @property
    def vec_output(self) -> str:
        """lines for control file listing vectors"""
        # results_filename: Path = self.results_loc / f"{self.name}.txt"
        vec_listing = ""  # initialize to blank

        if self.cmd_type == "ac":
            vec_listing = f"wrdata {self.results_filename} {self.vector}"
        if self.cmd_type == "dc":
            vec_listing = f"wrdata {self.results_filename} {self.vector}"
        if self.cmd_type == "disto":
            vec_listing = f"wrdata {self.results_filename} {self.vector}"
        if self.cmd_type == "noise":
            vec_listing = f"wrdata {self.results_filename} {self.vector}"
        if self.cmd_type == "op":
            vec_listing = f"print line {self.vector} > {self.results_filename}"
        if self.cmd_type == "pz":
            vec_listing = f"wrdata {self.results_filename} {self.vector}"
        if self.cmd_type == "sens":
            vec_listing = f"print line {self.vector} > {self.results_filename}"
        if self.cmd_type == "sp":
            vec_listing = f"wrdata {self.results_filename} {self.vector}"
        if self.cmd_type == "tf":
            vec_listing = f"print line {self.vector} > {self.results_filename}"
        if self.cmd_type == "tran":
            vec_listing = f"wrdata {self.results_filename} {self.vector}"

        return vec_listing

    def lines_for_cntl(self) -> list[str]:
        """returns a list of the command lines for the control file

        Returns:
            list[str]: command lines
        """
        return [self.cmd, self.vec_output]
