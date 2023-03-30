"""vectors.py unit test"""
import pytest
import ngspicehlp as ng


@pytest.mark.parametrize(
    "vec_input,expected_from_inputs",
    [
        (["sig1"], "Vectors(['sig1'])"),
        (["sig1", "sig2"], "Vectors(['sig1', 'sig2'])"),
        (["sig1", 1000, "sig2"], "Vectors(['sig1', '1000', 'sig2'])"),
        (["sig1  ", "sig2", "sig3", "sig2"], "Vectors(['sig1', 'sig2', 'sig3'])"),
        (["sig1    sig3 sig2"], "Vectors(['sig1', 'sig3', 'sig2'])"),
        ("sig1 sig3 sig2", "Vectors(['sig1', 'sig3', 'sig2'])"),
        ("sig1  sig3    sig2", "Vectors(['sig1', 'sig3', 'sig2'])"),
        (501, "Vectors(['501'])"),
        ("sig1 sig3 sig2 sig3 sig1", "Vectors(['sig1', 'sig3', 'sig2'])"),
    ],
)
def test_vectors_input(vec_input, expected_from_inputs):
    """vector with one signal initialized as a list"""
    my_vector = ng.Vectors(vec_input)
    assert repr(my_vector) == expected_from_inputs


def test_repr():
    """check __repr__ function"""
    my_vector = ng.Vectors(["sig1", "sig2"])
    assert repr(my_vector) == "Vectors(['sig1', 'sig2'])"


def test_str():
    """check __repr__ function"""
    my_vector = ng.Vectors(["sig1", "sig2", "sig3"])
    assert str(my_vector) == "sig1 sig2 sig3"


def test_vector_list_out():
    """check when outputing a list of the vectors"""
    vec1 = ng.Vectors(["sig1", " sig3 sig2"])
    assert vec1.list_out() == ["sig1", "sig3", "sig2"]


def test_vector_sort():
    """check sort function"""
    my_vector = ng.Vectors(["sig2", "sig3", "sig1"])
    my_vector.sort()
    assert str(my_vector) == "sig1 sig2 sig3"


def test_vector_union():
    """check union of vectors"""
    vec1 = ng.Vectors(["sig1", "sig2"])
    vec2 = ng.Vectors(["sig2", "sig3"])
    vec3 = ng.Vectors("0 4 sig10")
    vec3.union(vec1, vec2)
    assert str(vec3) == "0 4 sig10 sig1 sig2 sig3"


def test_vector_subtract():
    """check subtraction of vectro"""
    vec1 = ng.Vectors("0 4 sig10 sig1 sig2 sig3")
    vec2 = ng.Vectors(["sig2 4"])
    vec1.subtract(vec2)
    assert str(vec1) == "0 sig10 sig1 sig3"
