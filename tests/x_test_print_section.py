"""print_section.py unit test"""
import sys
from typing import Any
import pytest
from pytest import MonkeyPatch
import ngspicehlp as ng


@pytest.fixture
def capture_stdout(monkeypatch: MonkeyPatch) -> dict[str, Any]:
    "capture instead of printing to stdout"
    buffer: dict[str, Any] = {"stdout": "", "write_calls": 0}

    def fake_write(sss: int):
        buffer["stdout"] += sss
        buffer["write_calls"] += 1

    monkeypatch.setattr(sys.stdout, "write", fake_write)
    return buffer


def test_print_section(capture_stdout: dict[str, Any]):
    """check print_section with a fixture

    Args:
        capture_stdout (_type_): _description_
    """
    # build stuff for ng.print_section function
    dummy_title = "My Dummy Text"
    dummy_text = "line one\nline two\n"
    ng.print_section("My Dummy Text", dummy_text)

    # build expected
    line_title = f"--- {dummy_title} ---"
    last_line = "---------------------"
    expected = f"\n{line_title}\n{dummy_text}\n{last_line}\n\n"

    assert capture_stdout["stdout"] == expected
