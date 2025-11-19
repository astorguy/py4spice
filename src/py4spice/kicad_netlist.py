"""initialize and run Kicad cmd"""

import subprocess
from subprocess import CompletedProcess
from pathlib import Path


class KicadNetlist:
    """KiCad netlist export command"""

    def __init__(
        self, kicad_cmd: Path, sch_filename: Path, netlist_filename: Path
    ) -> None:
        self.kicad_cmd: Path = kicad_cmd  # Path to the KiCad executable
        self.sch_filename: Path = sch_filename
        self.netlist_filename: Path = netlist_filename

        # construct the command
        self.cmd_args: list[str] = [f"{self.kicad_cmd}"]
        self.cmd_args.append("sch")
        self.cmd_args.append("export")
        self.cmd_args.append("netlist")
        self.cmd_args.append("--output")
        self.cmd_args.append(f"{self.netlist_filename}")
        self.cmd_args.append("--format")
        self.cmd_args.append("spice")
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
        return subprocess.run(self.cmd_args, check=False)
