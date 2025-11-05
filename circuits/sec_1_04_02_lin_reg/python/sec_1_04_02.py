import tomllib
from pathlib import Path

import py4spice as spi

CONFIG_FILENAME = Path("/workspaces/py4spice/circuits/config.toml")
PROJECT_SECTION = "SEC_1_04_02"


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
    LOAD = "load"
    STIMULUS = "stimulus"
    SUPPLIES = "supplies"
    MODELS = "models"
    DUT = "dut"
    CONTROL = "control"
    TOP1 = "top1"

    # Keys for the vectors_dict
    VEC_ALL = "vec_all"
    VEC_ALL_EXPANDED = "vec_all_expanded"
    VEC_OUT = "vec_out"
    VEC_IN_OUT = "vec_in_out"
    VEC_INTEREST = "vec_interest"
    VEC_POWER_CALC = "vec_power_calc"
    VEC_ETA = "vec_eta"


def initialize() -> tuple[
    dict[str, Path], dict[str, spi.Netlist], dict[str, spi.Vectors]
]:
    """Initialize paths, netlists, and vectors dictionaries for the project."""
    # read config file and create config dictionary
    with open(CONFIG_FILENAME, "rb") as config_file:
        my_config = tomllib.load(config_file)

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
    nets_path: Path = paths_dict[Ky.NETLISTS_PATH]  # make shorter alias
    netlists_dict: dict[str, spi.Netlist] = {}  # create empty netlist dictionary

    netlists_dict[Ky.BLANKLINE] = spi.Netlist("")  # blank line for spacing
    netlists_dict[Ky.TITLE] = spi.Netlist("* Title line")  # title line
    netlists_dict[Ky.END_LINE] = spi.Netlist(".end")  # end statement

    # create netlist objects from files and add to netlist dictionary
    netlists_dict[Ky.DUT] = spi.Netlist(nets_path / "dut.cir")
    netlists_dict[Ky.LOAD] = spi.Netlist(nets_path / "load.cir")
    netlists_dict[Ky.STIMULUS] = spi.Netlist(nets_path / "stimulus.cir")
    netlists_dict[Ky.SUPPLIES] = spi.Netlist(nets_path / "supplies.cir")
    netlists_dict[Ky.MODELS] = spi.Netlist(nets_path / "models.cir")

    # Define a vector dictionary for simulation and post-simulation analysis
    vectors_dict = {
        Ky.VEC_ALL: spi.Vectors("all"),
        Ky.VEC_ALL_EXPANDED: spi.Vectors(
            "q1_base div e1#branch in out out_meas vee vee#branch vin#branch vmeas#branch ref vref#branch"
        ),
        Ky.VEC_IN_OUT: spi.Vectors("in out"),
        Ky.VEC_OUT: spi.Vectors("out"),
        Ky.VEC_INTEREST: spi.Vectors("in out div q1_base"),
        Ky.VEC_POWER_CALC: spi.Vectors("in vin#branch out vmeas#branch"),
        Ky.VEC_ETA: spi.Vectors("eta"),
    }
    return paths_dict, netlists_dict, vectors_dict


def main() -> None:
    # initialize paths, netlists, and vectors dictionaries
    paths_dict, netlists_dict, vectors_dict = initialize()

    # Part 1: Simulate and analyze
    # note: we pass back the netlists_dict because the top1 netlist was added to it
    netlists_dict = part1(paths_dict, netlists_dict, vectors_dict)


if __name__ == "__main__":
    main()
