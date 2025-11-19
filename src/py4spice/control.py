"""Create control file"""

import time
from pathlib import Path


class Control:
    """Generate Control file"""

    def __init__(self) -> None:
        self.beginning: list[str] = [".control"]
        self.beginning.extend([f"* Timestamp: {time.asctime()}"])
        self.beginning.extend(["set wr_singlescale  $ makes one x-axis for wrdata"])
        self.beginning.extend(["set wr_vecnames     $ puts names at top of columns"])

        self.ending: list[str] = ["quit"]
        self.ending.extend([".endc"])

        self.middle: list[str] = []

    def __str__(self) -> str:
        """output str of contents of control file

        Returns:
            str: contents of control file lines
        """
        content: list[str] = self.beginning + self.middle + self.ending
        return "\n".join(content)

    def __list_to_file(self, filename: Path, content: list[str]) -> None:
        """list to file with linefeeds between items"""

        with filename.open("w+", encoding="UTF-8") as _:
            for line in content:
                _.write(f"{line}\n")

    def insert_lines(self, lines: list[str]) -> None:
        """append line string to content

        Args:
            lines (str): line to add to control file
        """
        self.middle.extend(lines)

    def content_to_file(self, cntl_filename: Path) -> None:
        """write content to file"""
        content: list[str] = self.beginning + self.middle + self.ending
        self.__list_to_file(cntl_filename, content)
