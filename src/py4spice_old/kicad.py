"""initialize and run Kicad cmd"""
import subprocess
from subprocess import CompletedProcess
from pathlib import Path


class KicadCmd:
    """KiCad cmd"""

    def __init__(
        self, kicad_cmd: Path, sch_filename: Path, netlist_filename: Path
    ) -> None:
        self.kicad_cmd: Path = kicad_cmd
        self.sch_filename: Path = sch_filename
        self.netlist_filename: Path = netlist_filename

        self.cmd_args = [f"{self.kicad_cmd}"]
        self.cmd_args.append("sch")
        self.cmd_args.append("export netlist")
        self.cmd_args.append(f"--output {self.netlist_filename}")
        self.cmd_args.append("--format spice")
        self.cmd_args.append(f"{self.sch_filename}")
        self.cmd: str = " ".join(str(item) for item in self.cmd_args)

    def __str__(self) -> str:
        """print out the constructed KiCad cmd

        Returns:
            str: the cmd that has been contructed
        """
        return self.cmd

    def run(self) -> CompletedProcess[bytes]:
        """execute the kicad cmd"""
        return subprocess.run(self.cmd, check=True)
