from pathlib import Path
from typing import Optional


class Netlist:
    """Manipulates SPICE netlists"""

    def __init__(self, filename_or_string: Optional[Path | str] = None) -> None:
        self.data: list[str] = []
        if isinstance(filename_or_string, Path):
            with open(filename_or_string, "r") as file:
                self.data = [line.rstrip("\n").lower() for line in file.readlines()]
        if isinstance(filename_or_string, str):
            self.data = filename_or_string.lower().split("\n")

    def __str__(self) -> str:
        return "\n".join(self.data)

    def write_to_file(self, filename: Path) -> None:
        """ "Write netlist object data to a file"""
        with open(filename, "w") as file:
            file.write("\n".join(self.data))

    def __add__(self, other: "Netlist") -> "Netlist":
        """Concatenate netlists with + operator"""
        combined_data = self.data + other.data
        return Netlist("\n".join(combined_data))

    def delete_line(self, index: int) -> None:
        del self.data[index]

    def line_starts_with(self, string: str) -> int:
        """returns index of first line that starts with string"""
        for i, line in enumerate(self.data):
            if line.startswith(string):
                return i
        return -1

    def del_line_starts_with(self, string: str) -> None:
        """deletes first line that starts with string"""
        index = self.line_starts_with(string)
        if index != -1:
            del self.data[index]

    def insert_line(self, index: int, line: str) -> None:
        """inserts string line at index in data list"""
        self.data.insert(index, line.lower())

    def del_slash(self) -> None:
        """Deletes foward slashes in lines that begin with letters a through z
        regardless of case"""
        self.data = [
            line.replace("/", "") if line[0].isalpha() else line for line in self.data
        ]
