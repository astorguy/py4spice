"""kicad.py unit test"""

from pathlib import Path
import ngspicehlp as ng

PATH1 = Path("arg1")
PATH2 = Path("arg2")
PATH3 = Path("arg3")


def test_kicad_cmd_str():
    """test constructed kicad command"""
    good_cmd_list: list[str] = []
    good_cmd_list.append(f"{PATH1}")
    good_cmd_list.append("sch")
    good_cmd_list.append("export netlist")
    good_cmd_list.append("--output")
    good_cmd_list.append(f"{PATH3}")
    good_cmd_list.append("--format spice")
    good_cmd_list.append(f"{PATH2}")
    good_cmd: str = " ".join(str(item) for item in good_cmd_list)

    kicad_cmd1 = ng.KicadCmd(PATH1, PATH2, PATH3)
    assert str(kicad_cmd1) == good_cmd
