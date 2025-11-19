def test_basic_import():
    import py4spice

    assert hasattr(py4spice, "Simulate")
