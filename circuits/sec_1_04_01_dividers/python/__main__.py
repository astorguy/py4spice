import tomllib
from pathlib import Path

import py4spice as spi

CONFIG_FILENAME = Path("/workspaces/py4spice/circuits/config.toml")
PROJECT_SECTION = "SEC_1_04_01"


class Ky:
    """Keys for dictionaries.  Defined here at top level so they can be
    referenced instead of using strings for keys.
    """

    # Keys for decoding config file
    GLOBAL = "GLOBAL"
    PROJECT = "PROJECT"
    NGSPICE_EXE_STR = "NGSPICE_EXE_STR"
    NETLISTS_DIR_STR = "NETLISTS_DIR_STR"
    RESULTS_DIR_STR = "RESULTS_DIR_STR"
    SIM_TRANSCRIPT_STR = "SIM_TRANSCRIPT_STR"
    PROJ_PATH_STR = "PROJ_PATH_STR"

    # Keys for the paths_dict
    NGSPICE_EXE = "ngspice_exe"
    PROJ_PATH = "proj_path"
    NETLISTS_PATH = "netlists_path"
    RESULTS_PATH = "results_path"
    SIM_TRANSCRIPT_FILENAME = "sim_transcript_filename"

    # Keys for the netlists_dict
    BLANKLINE = "blankline"
    TITLE = "title"
    END_LINE = "end_line"
    STIMULUS = "stimulus"
    SUPPLIES = "supplies"
    DUT = "dut"
    CONTROL = "control"
    TOP1 = "top1"

    # Keys for the vectors_dict
    VEC_ALL = "vec_all"
    VEC_ALL_EXPANDED = "vec_all_expanded"
    VEC_VIN = "vec_vin"
    VEC_IIN = "vec_iin"
    VEC_VOUT1 = "vec_vout1"
    VEC_VOUT2 = "vec_vout2"
    VEC_IOUT1 = "vec_iout1"
    VEC_IOUT2 = "vec_iout2"
    VEC_IN_OUT = "vec_in_out"


def initialize() -> tuple[
    dict[str, Path], dict[str, spi.Netlist], dict[str, spi.Vectors]
]:
    """Initialize paths, netlists, and vectors dictionaries for the project."""
    with open(CONFIG_FILENAME, "rb") as config_file:
        my_config = tomllib.load(config_file)

    # Create project path
    proj_path = Path(my_config[PROJECT_SECTION][Ky.PROJ_PATH_STR])

    # Create paths based on the config dictionary
    ngspice_exe: Path = Path(my_config[Ky.GLOBAL][Ky.NGSPICE_EXE_STR])
    netlists_path: Path = proj_path / my_config[Ky.GLOBAL][Ky.NETLISTS_DIR_STR]
    results_path: Path = proj_path / my_config[Ky.GLOBAL][Ky.RESULTS_DIR_STR]

    # create results directory if it does not exist
    results_path.mkdir(parents=True, exist_ok=True)

    # create simlulation transcript file. If it exists, make sure it is empty
    sim_tran_filename: Path = results_path / my_config[Ky.GLOBAL][Ky.SIM_TRANSCRIPT_STR]
    if sim_tran_filename.exists():  # delete and recreate. this makes sure it's empty
        sim_tran_filename.unlink()
    sim_tran_filename.touch()

    # create paths dictionary
    paths_dict = {
        Ky.NGSPICE_EXE: ngspice_exe,
        Ky.PROJ_PATH: proj_path,
        Ky.NETLISTS_PATH: netlists_path,
        Ky.RESULTS_PATH: results_path,
        Ky.SIM_TRANSCRIPT_FILENAME: sim_tran_filename,
    }

    # netlists_dict = define_netlists(paths_dict)
    netlists_path: Path = paths_dict[Ky.NETLISTS_PATH]  # make shorter alias
    netlists_dict: dict[str, spi.Netlist] = {}  # create empty netlist dictionary

    netlists_dict[Ky.BLANKLINE] = spi.Netlist("")  # blank line for spacing
    netlists_dict[Ky.TITLE] = spi.Netlist("* Title line")  # title line
    netlists_dict[Ky.END_LINE] = spi.Netlist(".end")  # end statement

    # create netlist objects from files and add to netlist dictionary
    netlists_dict[Ky.DUT] = spi.Netlist(netlists_path / "dut.cir")
    netlists_dict[Ky.STIMULUS] = spi.Netlist(netlists_path / "stimulus.cir")
    netlists_dict[Ky.SUPPLIES] = spi.Netlist(netlists_path / "supplies.cir")

    print(f"Project path: {proj_path}")
    print(f"Product section: {PROJECT_SECTION}")
    print(f"NGSPICE executable: {ngspice_exe}")
    print(f"Netlists path: {netlists_path}")
    print(f"Results path: {results_path}")

    # Define a vector dictionary for simulation and post-simulation analysis
    vectors_dict = {
        Ky.VEC_ALL: spi.Vectors("all"),
        Ky.VEC_ALL_EXPANDED: spi.Vectors(
            "in out1 out1_meas out2 out2_meas vee vee#branch vin#branch vmeas1#branch vmeas2#branch"
        ),
        Ky.VEC_VIN: spi.Vectors("in"),
        Ky.VEC_IIN: spi.Vectors("vin#branch"),
        Ky.VEC_VOUT1: spi.Vectors("out1"),
        Ky.VEC_VOUT2: spi.Vectors("out2"),
        Ky.VEC_IOUT1: spi.Vectors("vmeas1#branch"),
        Ky.VEC_IOUT2: spi.Vectors("vmeas2#branch"),
    }
    # create this vector as a combination of the other vectors
    vectors_dict[Ky.VEC_IN_OUT] = (
        vectors_dict[Ky.VEC_VIN]
        + vectors_dict[Ky.VEC_VOUT1]
        + vectors_dict[Ky.VEC_VOUT2]
    )
    return paths_dict, netlists_dict, vectors_dict


def main():
    paths_dict, netlists_dict, vectors_dict = initialize()


if __name__ == "__main__":
    main()
