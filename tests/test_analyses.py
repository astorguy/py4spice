"""analyes.py unit test"""

from pathlib import Path

# import pytest
import py4spice as spi


# @pytest.mark.skip(reason="WIP")
def test_input() -> None:
    """vector with one signal initialized as a list"""

    vec_all = spi.Vectors("all")
    results_path = Path("../fred")

    # computed
    my_analysis = spi.Analyses("a1", "op", "op", vec_all, results_path)

    assert my_analysis.vec_output == "print line all > ../fred/a1.txt"
