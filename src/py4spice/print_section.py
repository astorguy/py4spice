"""section off text so it is easier to read in terminal
"""
from typing import Any


def print_section(title: str, stuff: Any) -> None:
    """section off text so it is easier to read in terminal

    Args:
        title (str): name of the section
        stuff (Any): stuff to be printed
    """
    title_bar: str = f"--- {title} ---"
    print()
    print(title_bar)
    print(stuff)
    print("-" * len(title_bar))
    print()
