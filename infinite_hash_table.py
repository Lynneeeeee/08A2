from __future__ import annotations
from typing import Generic, TypeVar

from data_structures.referential_array import ArrayR

K = TypeVar("K")
V = TypeVar("V")

class InfiniteHashTable(Generic[K, V]):
    """
    Infinite Hash Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    TABLE_SIZE = 27

    def __init__(self) -> None:
        self.level = 0
        self.table = [None] * self.TABLE_SIZE

    def hash(self, key: K) -> int:
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE-1)
        return self.TABLE_SIZE-1

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """

        raise KeyError(key)

    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """
        raise KeyError(key)

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        raise KeyError(key)

    def __len__(self):
        raise KeyError(key)

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        items = []
        for slot in self.table:
            for key, value in slot:
                items.append(f"[{key}, {value}]")
        return"[" + ", ".join(items) + "]"

    def get_location(self, key) -> list[int]:
        """
        Get the sequence of positions required to access this key.

        :raises KeyError: when the key doesn't exist.
        """
        locations = []
        for level in range(4):
            self.level = level
            position = self.hash(key)
            if self.table[position] is None:  # the key doesn't exist
                raise KeyError(key)
            locations.append(position)
        return locations

    def __contains__(self, key: K) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See linear probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True
