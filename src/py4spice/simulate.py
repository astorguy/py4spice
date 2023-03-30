"""setup or run an ngspice simulation
"""
import subprocess
from pathlib import Path


class Simulate:
    """ngspice simulation"""

    def __init__(self, ngspice_exe: Path, netlist_filename: Path) -> None:

        self.ngspice_exe: Path = ngspice_exe
        self.netlist_filename: Path = netlist_filename

    @property
    def ngspice_command(self) -> str:
        """complete ngspice command"""
        return f"{self.ngspice_exe} {self.netlist_filename}"

    def __str__(self) -> str:
        return self.ngspice_command

    def run(self) -> None:
        """execute the simulation"""
        subprocess.run(self.ngspice_command, check=True)
