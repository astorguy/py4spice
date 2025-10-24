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
    netlists_dict[Ky.TITLE] = spi.Netlist("* voltage divider, section 1.4.1")  # title line
    netlists_dict[Ky.END_LINE] = spi.Netlist(".end")  # end statement

    # create netlist objects from files and add to netlist dictionary
    netlists_dict[Ky.DUT] = spi.Netlist(netlists_path / "dut.cir")
    netlists_dict[Ky.STIMULUS] = spi.Netlist(netlists_path / "stimulus.cir")
    netlists_dict[Ky.SUPPLIES] = spi.Netlist(netlists_path / "supplies.cir")

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


def part1(
    my_paths_dict: dict[str, Path],
    my_netlists_dict: dict[str, spi.Netlist],
    my_vectors_dict: dict[str, spi.Vectors],
) -> dict[str, spi.Netlist]:
    # Define analyses
    list_of_analyses: list[spi.Analyses] = []  # start with an empty list

    # 1st analysis: operating point
    op1 = spi.Analyses(
        name="op1",
        cmd_type="op",
        cmd="op",
        vector=my_vectors_dict[Ky.VEC_ALL],
        results_loc=my_paths_dict[Ky.RESULTS_PATH],
    )
    list_of_analyses.append(op1)

    # create control section
    my_control = spi.Control()  # create 'my_control' object
    for analysis in list_of_analyses:
        my_control.insert_lines(analysis.lines_for_cntl())
    my_netlists_dict[Ky.CONTROL] = spi.Netlist(str(my_control))

    # concatenate all tne netlists to make top1 and add to netlist dict
    my_netlists_dict[Ky.TOP1] = (
        my_netlists_dict[Ky.TITLE]
        + my_netlists_dict[Ky.BLANKLINE]
        + my_netlists_dict[Ky.DUT]
        + my_netlists_dict[Ky.BLANKLINE]
        + my_netlists_dict[Ky.SUPPLIES]
        + my_netlists_dict[Ky.BLANKLINE]
        + my_netlists_dict[Ky.STIMULUS]
        + my_netlists_dict[Ky.BLANKLINE]
        + my_netlists_dict[Ky.BLANKLINE]
        + my_netlists_dict[Ky.CONTROL]
        + my_netlists_dict[Ky.END_LINE]
        + my_netlists_dict[Ky.BLANKLINE]
    )
    # write netlist to a file so ngspice can read it
    # top_filename: Path = my_paths_dict[Ky.NETLISTS_PATH] / "top1.cir"
    top_filename: Path = my_paths_dict[Ky.NETLISTS_PATH] / (Ky.TOP1 + ".cir")
    my_netlists_dict[Ky.TOP1].write_to_file(top_filename)

    # prepare simulate object, print out command, and simulate
    sim: spi.Simulate = spi.Simulate(
        ngspice_exe=my_paths_dict[Ky.NGSPICE_EXE],
        netlist_filename=top_filename,
        transcript_filename=my_paths_dict[Ky.SIM_TRANSCRIPT_FILENAME],
        name="sim1",
        timeout=20,
    )
    # spi.print_section("Ngspice Command", sim1) # print out command
    sim.run()  # run the Ngspice simulation

    # convert the raw results into list of SimResults objects
    sim_results: list[spi.SimResults] = [
        spi.SimResults.from_file(analysis.cmd_type, analysis.results_filename)
        for analysis in list_of_analyses
    ]
    (my_op1,) = sim_results  # give each SimResults object an easier name

    # diaplay results for operating point analysis
    spi.print_section("Operating Point Results", my_op1.table_for_print())

    # Calculate power and efficiency
    vin: float = my_op1.data_table[str(my_vectors_dict[Ky.VEC_VIN])]
    iin: float = my_op1.data_table[str(my_vectors_dict[Ky.VEC_IIN])]
    vout1: float = my_op1.data_table[str(my_vectors_dict[Ky.VEC_VOUT1])]
    vout2: float = my_op1.data_table[str(my_vectors_dict[Ky.VEC_VOUT2])]
    iout1: float = my_op1.data_table[str(my_vectors_dict[Ky.VEC_IOUT1])]
    iout2: float = my_op1.data_table[str(my_vectors_dict[Ky.VEC_IOUT2])]

    pr1: float = (vin - vout1) * iout1
    pr2: float = (vin - vout2) * iout2
    pout1: float = vout1 * iout1
    pout2: float = vout2 * iout2
    pout: float = pout1 + pout2
    pin: float = vin * -iin
    eta: float = pout / pin

    print(f"p1 = {pr1:.4g}W")
    print(f"p2 = {pr2:.4g}W")
    print(f"pout1 = {pout1:.4g}W")
    print(f"pout2 = {pout2:.4g}W")
    print(f"pout = {pout:.4g}W")
    print(f"pin = {pin:.4g}W")
    print(f"eta = {eta * 100:.4g}%")

    return my_netlists_dict


def main():
    # initialize paths, netlists, and vectors dictionaries
    paths_dict, netlists_dict, vectors_dict = initialize()

    # Part 1: Simulate and analyze a resistive divider
    # note: we pass back the netlists_dict because the top1 netlist was added to it
    netlists_dict = part1(paths_dict, netlists_dict, vectors_dict)


if __name__ == "__main__":
    main()
