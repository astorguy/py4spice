"""setup or run an ngspice simulation"""

import datetime
import subprocess
from pathlib import Path


class Simulate:
    """ngspice simulation"""

    def __init__(
        self,
        ngspice_exe: Path,
        netlist_filename: Path,
        transcript_filename: Path,
        name: str,
        timeout: int = 20,  # Default 20 seconds
    ) -> None:
        self.ngspice_exe: Path = ngspice_exe
        self.netlist_filename: Path = netlist_filename
        self.transcript_filename: Path = transcript_filename
        self.name: str = name
        self.timeout: int = timeout
        self.transcript_content: str = (
            f"\n-----------------\nSimulation name: {self.name}"
        )

    @property
    def ngspice_command(self) -> list[str]:
        """define the ngspice command"""
        return [str(self.ngspice_exe), "-b", str(self.netlist_filename)]

    def __str__(self) -> str:
        return " ".join(self.ngspice_command)

    def run(self) -> None:
        """Execute the ngspice simulation"""
        try:
            completed_sim = subprocess.run(
                self.ngspice_command,
                capture_output=True,
                check=True,
                text=True,
                timeout=self.timeout,
            )
            # add timestamp to transcript
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.transcript_content += f"\nTimestamp: {timestamp}\n"

            # add simulation output to transcript
            self.transcript_content += completed_sim.stdout

            # append transcript to transcript file
            with open(self.transcript_filename, "a") as file:
                file.write(self.transcript_content)

        except subprocess.TimeoutExpired:
            print("Simulation timed out.")
