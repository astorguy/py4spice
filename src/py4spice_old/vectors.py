"""Vector set of signals for which to gather data, plot, ... """

from typing import TypeVar

# used to get rid of type errors from static error checking (mypy, etc.)
T = TypeVar("T", bound="Vectors")


class Vectors:
    """Vectors are a list of signals to specified for simulation, display, ..."""

    def __init__(self, vect_init: list[str | int] | str | int):
        self.__vect = []
        if isinstance(vect_init, list):
            self.__vect = [str(signal) for signal in vect_init]
            self._words_to_items()
        if isinstance(vect_init, str):
            self.__vect = vect_init.split()
        if isinstance(vect_init, int):
            self.__vect = [str(vect_init)]
        self._remove_dups()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__vect})"

    def __str__(self) -> str:
        return " ".join(self.__vect)

    def _words_to_items(self) -> None:
        """Convert words separated by spaces into separate list items"""
        my_list: list[str] = []
        for item in self.__vect:
            if " " in item:
                # Split the string into multiple items
                split_items = item.split()
                # Add the new items to the new list
                my_list.extend(split_items)
            else:
                my_list.append(item)
        self.__vect = my_list

    def _remove_dups(self) -> None:
        """remove duplicate signals"""
        my_list = self.__vect
        no_dups: list[str] = []
        for item in my_list:
            if item not in no_dups:
                no_dups.append(item)
        self.__vect = no_dups

    def list_out(self) -> list[str]:
        """Outputs vector as a list

        Returns:
            list[str]:
        """
        return self.__vect

    def sort(self) -> None:
        """Sort the signals"""
        self.__vect = sorted(self.__vect)

    def union(self: T, *vecs: T) -> None:
        """Combine the vector object with others passed in

        Args:
            *vecs (vectors): one or more vectors to union
        """
        for vec in vecs:
            self.__vect = self.__vect + vec.list_out()
            self._remove_dups()

    def subtract(self: T, vec2: T) -> None:
        """Remove from this vector the signals in the second one

        Args:
            self (vectors): vector to subtract from
            vec2 (vectors): vector to subtract out
        """
        list1 = self.list_out()
        list2 = vec2.list_out()
        self.__vect = [item for item in list1 if item not in list2]
        self._remove_dups()
