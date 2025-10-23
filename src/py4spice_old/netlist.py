"""Python project"""

from pathlib import Path
from typing import Optional

# these are used in main for testing
INPUT_FILE = "./nand.cir"
OUTFILE_FILE = "./nand2.cir"
REMOVE_TITLE_END = True
SUBCKT = True


class Netlist:
    """Read netlist, correct, and write new one"""

    def __init__(self, input_file: Optional[Path] = None) -> None:
        self.netlist_data: list[list[str]] = [[]]
        if input_file:
            self.readfile(input_file)

    def __str__(self) -> str:
        """write the netlist data to a file"""
        list_of_lines: list[str] = [" ".join(lines) for lines in self.netlist_data]
        return "\n".join(list_of_lines)

    def readfile(self, filename: Path) -> None:
        """read a file and create the netlist data"""
        file_text: str = filename.read_text()
        lines: list[str] = file_text.splitlines()
        self.netlist_data = [word.split() for word in lines]

    def insert_line(self, index: int, new_line: str) -> None:
        """insert one or more lines into netlist"""
        words: list[str] = new_line.split()
        self.netlist_data.insert(index, words)

    def remove_forwardslashes(self) -> None:
        """remove forwardslashes form the node names"""

        self.netlist_data = [
            [word.lstrip("/") if word.startswith("/") else word for word in lines]
            for lines in self.netlist_data
        ]

    def remove_first_last_lines(self) -> None:
        """remove first line (title) and last line (.end)"""
        del self.netlist_data[0]
        del self.netlist_data[-1]

    def create_subckt(self) -> None:
        "look for .subckt line, if exists, make netlist a subckt"

        target = ".subckt"

        target_index = None

        for line_index, line_list in enumerate(self.netlist_data):
            if line_list[0] == target:
                target_index = line_index
                break
        if target_index:
            target_line_list = self.netlist_data.pop(target_index)
            self.netlist_data.insert(0, target_line_list)
            target_2nd_word = self.netlist_data[0][1]
            self.netlist_data.append([".ends", target_2nd_word])

    def writefile(self, filename: Path) -> None:
        """write the netlist data to a file"""
        list_of_lines: list[str] = [" ".join(lines) for lines in self.netlist_data]
        big_string: str = "\n".join(list_of_lines)
        filename.write_text(big_string, "UTF-8")


def main() -> None:
    """testing code"""
    in_file = Path(INPUT_FILE)
    out_file = Path(OUTFILE_FILE)
    netlist1 = Netlist()
    netlist1.readfile(in_file)

    netlist1.remove_forwardslashes()

    if REMOVE_TITLE_END:
        netlist1.remove_first_last_lines()

    if SUBCKT:
        netlist1.create_subckt()

    netlist1.writefile(out_file)


if __name__ == "__main__":
    main()
