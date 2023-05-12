from __future__ import annotations
from typing import Generic, TypeVar

from data_structures.hash_table import LinearProbeTable
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

    def __init__(self, level: int = 0) -> None:
        self.level = level
        self.table_size = self.TABLE_SIZE
        self.table: ArrayR[tuple[K, V] | InfiniteHashTable[K, V]] = ArrayR(self.table_size)
        self.count = 0

    def hash(self, key: K) -> int:
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE - 1)
        return self.TABLE_SIZE - 1

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key
        :Parameter: key
        :Complexity: O(1)
        :raises KeyError: when the key doesn't exist.
        """
        if len(key) == 0:
            raise KeyError("Key cannot be empty")
        index = self.hash(key)

        if self.table[index] is None:
            raise KeyError("Key does not exist")

        if isinstance(self.table[index], InfiniteHashTable):
            return self.table[index][key]
        elif self.table[index][0] == key:
            return self.table[index][1]
        else:
            raise KeyError("Key does not exist")

    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        :Parameter: key, value
        :Complexity: O(1)
        :raises KeyError: when the key is empty.
        """
        if len(key) == 0:
            raise KeyError("Key cannot be empty")

        index = self.hash(key)
        if self.table[index] is None:
            self.table[index] = (key, value)
            self.count += 1
        elif isinstance(self.table[index], InfiniteHashTable):
            self.table[index][key] = value
            self.count += 1
        elif self.table[index][0] == key:
            self.table[index] = (key, value)
        else:
            temp_pair = self.table[index]
            self.table[index] = InfiniteHashTable(self.level + 1)
            self.table[index][temp_pair[0]] = temp_pair[1]
            self.table[index][key] = value
            self.count += 1

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.
        :Parameter: key
        :Complexity: O(1)
        :raises KeyError: when the key doesn't exist.
        """
        if len(key) == 0:
            raise KeyError("Key cannot be empty")

        index = self.hash(key)

        if self.table[index] is None:
            raise KeyError("Key does not exist")

        if isinstance(self.table[index], InfiniteHashTable):
            del self.table[index][key]
            self.count -= 1
            if len(self.table[index]) == 1:
                inner_pair = self.table[index].get_first_pair()
                self.table[index] = inner_pair

        elif self.table[index][0] == key:
            self.table[index] = None
            self.count -= 1
        else:
            raise KeyError("Key does not exist")

    def get_first_pair(self):
        """
        Get the first pair
        :Complexity: O(N)
        """
        for i in self.table:
            if i:
                return i

    def __len__(self):
        """
        Return the length of table
        :Complexity: O(1)
        """
        return self.count

    def __str__(self) -> str:
        """
        String representation.
        Not required but may be a good testing tool.
        :Complexity: O(1)
        """
        return str(self.table)

    def get_location(self, key) -> list[int]:
        """
        Get the sequence of positions required to access this key.
        :Parameter: key
        :Complexity: O(N)
        :raises KeyError: when the key doesn't exist.
        """
        if len(key) == 0:
            raise KeyError("Key does not exist")

        index = self.hash(key)
        if self.table[index] is None:
            raise KeyError("Key does not exist")

        if isinstance(self.table[index], InfiniteHashTable):
            return [index] + self.table[index].get_location(key)
        elif self.table[index][0] == key:
            return [index]
        else:
            raise KeyError("Key does not exist")

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
