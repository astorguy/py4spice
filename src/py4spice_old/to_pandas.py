"""Ngspice simulation results to Pandas"""

from pathlib import Path
import pandas as pd


def _op_to_pandas(my_filename: Path) -> pd.DataFrame:
    """converts the op (operating point) results to a Pandas DF

    Args:
        my_filename (Path): the op file

    Returns:
        pd.DataFrame:
    """
    # create an empty dictionary
    my_dict: dict[str, float] = {}

    # read the text file and split the lines by newline
    file_text: str = my_filename.read_text()
    lines: list[str] = file_text.split("\n")

    # create a dictionary to store the key-value pairs
    for line in lines:
        if line:
            key, value = line.split("=")
            key = key.replace(" ", "")
            value = value.replace(" ", "")
            my_dict[key] = float(value)

    return pd.DataFrame.from_dict(my_dict, orient="index", columns=["Value"])


def to_pandas(
    results_loc: Path,
    ng_result_name: str,
    ng_result_type: str,
    del_results_file: bool = False,
) -> pd.DataFrame:
    """converts simulation result to list of Pandas dataframe
    Args:
        results_loc (Path):
        ng_result_name (str):
        ng_result_type (str):
        del_results_file (bool, optional): deletes results file after conversion.
                                           defaults to False.
    Returns:
        list[pd.DataFrame]:
    """

    results_filename: Path = results_loc / f"{ng_result_name}.txt"
    if ng_result_type == "op":
        this_df: pd.DataFrame = _op_to_pandas(results_filename)
    else:
        this_df = pd.read_csv(results_filename, delim_whitespace=True)

    # Want to delete raw text files after converting to Pandas?
    if del_results_file:
        results_filename.unlink()

    return this_df
