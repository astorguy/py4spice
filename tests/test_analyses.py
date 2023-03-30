"""analyes.py unit test"""
from pathlib import Path
import ngspicehlp as ng


def test_input() -> None:
    """vector with one signal initialized as a list"""

    vec_all = ng.Vectors("all")
    results_path = Path("../fred")

    # computed
    my_analysis = ng.Analyses("a1", "op", ["op"], vec_all, results_path)

    assert my_analysis.vec_output == "print line all > ..\\fred\\a1.txt"
