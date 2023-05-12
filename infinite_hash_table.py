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
        self.table = {}

    def hash(self, key: K) -> int:
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE-1)
        return self.TABLE_SIZE-1

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key
        :Parameter: key
        :Complexity: O(1)
        :raises KeyError: when the key doesn't exist.
        """
        if len(key) == 0:
            raise KeyError("Key does not exist")

        index = self.hash(key)
        if index not in self.table:
            raise KeyError("Key does not exist")

        if len(key) == 1:
            return self.table[index]
        else:
            return self.table[index].__getitem__(key)

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
        if index not in self.table:
            self.table[index] = InfiniteHashTable()
            self.table[index].key = key
            self.table[index].value = value
        else:
            self.table[index] = InfiniteHashTable(self.level + 1)
            self.table[index].__setitem__(key, value)
        # if len(key) == 1:
        #     self.table[index] = value
        # else:
        #     if not isinstance(self.table.get(index), InfiniteHashTable):
        #         self.table[index] = InfiniteHashTable(self.level + 1)
        #     self.table[index].__setitem__(key[1:], value)

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
        if index in self.table:
            if len(key) == 1:
                del self.table[index]
            else:
                subtable = self.table[index]
                if isinstance(subtable, InfiniteHashTable):
                    del subtable[key[1:]]
                else:
                    raise KeyError("Key does not exist")
        else:
            raise KeyError("Key does not exist")

    def __len__(self):
        return sum(len(subtable) if isinstance(subtable, InfiniteHashTable) else 1 for subtable in self.table.values())

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
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
        # print('hi')
        # print(index in self.table)
        if index in self.table:
            if len(key) == 1:
                return [index]
            else:
                print(self.table[index])
                return [index] + self.table[index].get_location(key)
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


if __name__ == '__main__':
    ih = InfiniteHashTable()
    ih["lin"] = 1
    print(ih.get_location("lin"))
    # ih["leg"] = 2
    #
    # print(ih.get_location("leg"))