from __future__ import annotations

from typing import Generic, TypeVar, Iterator
from data_structures.hash_table import LinearProbeTable, FullError
from data_structures.referential_array import ArrayR

K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')


class DoubleKeyTable(Generic[K1, K2, V]):
    """
    Double Hash Table.

    Type Arguments:
        - K1:   1st Key Type. In most cases should be string.
                Otherwise `hash1` should be overwritten.
        - K2:   2nd Key Type. In most cases should be string.
                Otherwise `hash2` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241,
                   786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes: list | None = None, internal_sizes: list | None = None) -> None:

        """
        O(n)
        if we know the size of self.sizes and internal_sizes, otherwise we will use the TABLE_SIZES
        the first element in the "size" list is the starting point of the table size, represented the initial size of
        the main table, same as the self.internal_sizes[0].
        self.table is used to create an empty hash table with a predefined size.
        parameter: sizes, internal_sizes
        """
        if sizes is not None:
            self.TABLE_SIZES = sizes
        self.internal_sizes = internal_sizes
        self.top_level_table = LinearProbeTable[K1, LinearProbeTable[K2, V]](self.TABLE_SIZES)
        self.count = 0

    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
        """
        Hash the 2nd key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % sub_table.table_size
            a = a * self.HASH_BASE % (sub_table.table_size - 1)
        return value

    def _linear_probe(self, key1: K1, key2: K2, is_insert: bool) -> tuple[int, int]:
        """

        Find the correct position for this key in the hash table using linear probing.

        :raises KeyError: When the key pair is not in the table, but is_insert is False.
        :raises FullError: When a table is full and cannot be inserted.

        stores the returned position in outer_pos.
        Create a new inner hash table
        Create a tuple with key1 and the new inner hash table
        Assign the tuple to the outer hash table at the outer_pos index
        :parameter: key1. key2, is_insert
        :return: tuple[int, int]
        :complexity: O(m + n)
        """
        self.top_level_table.hash = self.hash1

        outer_pos = self.top_level_table._linear_probe(key1, is_insert)
        if is_insert:
            try:
                inner_pos = self.top_level_table[key1]._linear_probe(key2, is_insert)
            except KeyError:
                temp = LinearProbeTable(self.internal_sizes)
                temp.hash = lambda k: self.hash2(k, temp)
                inner_pos = temp._linear_probe(key2, is_insert)
        else:
            inner_pos = self.top_level_table[key1]._linear_probe(key2, is_insert)
        return (outer_pos, inner_pos)

        # if is_insert:
        #     if self.top_level_table.array[outer_pos] is None:
        #         inner_hash_table = LinearProbeTable[key2, V](sizes=self.internal_sizes)
        #         inner_hash_table.hash = lambda k: self.hash2(k, inner_hash_table)
        #         key_and_inner_hash_table = (key1, inner_hash_table)
        #
        #         self.top_level_table.array[outer_pos] = key_and_inner_hash_table
        #
        # bottom_level_table = self.top_level_table.array[outer_pos][1]
        # inner_pos = bottom_level_table._linear_probe(key2, is_insert)
        # return (outer_pos, inner_pos)

        # index1 = self.hash1(key1)
        # sub_table = self.table[index1]
        #
        # if sub_table is None:
        #     if is_insert:
        #         sub_table = LinearProbeTable[K2, V](self.internal_size)
        #         self.table[index1] = sub_table[0]
        #     else:
        #         index2 = sub_table.table_size  # Use table_size as a sentinel value
        #         return index1, index2
        #
        # index2 = self.hash2(key2, sub_table)
        # for i in range(sub_table.table_size):
        #     if sub_table.array[index2] is None:
        #         if is_insert:
        #             break
        #         else:
        #             index2 = sub_table.table_size  # Use table_size as a sentinel value
        #             break
        #     elif sub_table.array[index2][0] == key2:
        #         break
        #     else:
        #         index2 = (index2 + 1) % sub_table.table_size
        # else:
        #     if is_insert:
        #         index2 = sub_table.table_size  # Use table_size as a sentinel value
        #
        # return index1, index2

        # raise NotImplementedError()

    def iter_keys(self, key: K1 | None = None) -> Iterator[K1 | K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.

        method: if key is none, iterate over all top-level keys
        else, find the bottom-level table for the given top-level key
        then iterate over all keys in the bottom-level table and yield the bottom-level key
        :param key: The top-level key or None
        :return: Iterator[K1|K2]
        :complexity: O(m + n)
        """
        self.top_level_table.hash = self.hash1
        if key is None:
            for start in self.top_level_table.array:
                if start is not None:
                    yield start[0]
        else:
            outer_pos = self.top_level_table._linear_probe(key, False)
            bottom_level_table = self.top_level_table.array[outer_pos][1]

            for start in bottom_level_table.array:
                if start is not None:
                    yield start[0]
        # raise NotImplementedError()

    def keys(self, key: K1 | None = None) -> list[K1]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.
        :param key: The top-level key or None
        :return: A list of keys (either top-level or bottom-level)
        :complexity: O(m+n)
    """
        self.top_level_table.hash = self.hash1
        if key is None:
            return list(self.iter_keys())
        else:
            return list(self.iter_keys(key))
            # raise NotImplementedError()

    def iter_values(self, key: K1 | None = None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.

        :param key: The top-level key or None
        :return: Iterator[V]
        :complexity: O(m*n)
        """
        self.top_level_table.hash = self.hash1
        if key is None:
            for start in self.top_level_table.array:
                if start is not None:
                    bottom_level_table = start[1]
                    for inner_start in bottom_level_table.array:
                        if inner_start is not None:
                            yield inner_start[1]
        else:
            outer_pos = self.top_level_table._linear_probe(key, False)
            bottom_level_table = self.top_level_table.array[outer_pos][1]

            for start in bottom_level_table.array:
                if start is not None:
                    yield start[1]

        # raise NotImplementedError()

    def values(self, key: K1 | None = None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.

        :param key: The top-level key or None
        :return: A list of values (either top-level or bottom-level)
        :complexity: O(m*n)
        """

        return list(self.iter_values(key))

        # raise NotImplementedError()

    def __contains__(self, key: tuple[K1, K2]) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See linear probe.
        """
        self.top_level_table.hash = self.hash1
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: tuple[K1, K2]) -> V:
        """
        Get the value at a certain key

        method: Check if the inner hash table exists for the given outer_key
        Check if the inner_key exists in the inner hash table
        :raises KeyError: when the key doesn't exist.
        :parameter: key: tuple[K1, K2]
        :return: value
        :complexity: O(m+n)
        """
        self.top_level_table.hash = self.hash1
        k1, k2 = key
        outer_pos = self.top_level_table._linear_probe(k1, False)

        if self.top_level_table.array[outer_pos] is None:
            raise KeyError

        inner_hash_table = self.top_level_table.array[outer_pos][1]
        inner_pos = inner_hash_table._linear_probe(k2, False)

        if inner_hash_table.array[inner_pos] is None:
            raise KeyError

        return inner_hash_table.array[inner_pos][1]
        # raise NotImplementedError()

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        method: Check if the inner hash table exists for the given outer_key
        If it doesn't exist, create a new inner hash table and insert it into the outer hash table
        Insert the inner_key into the inner hash table
        :parameter: key: tuple[K1, K2], data: V
        :complexity: O(m+n)
        """
        # k1, k2 = key
        # outer_pos = self.top_level_table._linear_probe(k1, False)
        #
        # if self.top_level_table.array[outer_pos] is None:
        #     inner_hash_table = LinearProbeTable[K2, V](sizes=self.internal_sizes)
        #     inner_hash_table.hash = lambda k: self.hash2(k, inner_hash_table)
        #     self.top_level_table.array[outer_pos] = (k1, inner_hash_table)
        # else:
        #     inner_hash_table = self.top_level_table.array[outer_pos][1]
        #
        # inner_hash_table[k2] = data
        # # raise NotImplementedError()

        k1, k2 = key
        self.top_level_table.hash = self.hash1
        try:
            self.top_level_table[k1]
        except KeyError:
            inner_hash_table = LinearProbeTable[K2, V](self.internal_sizes)
            inner_hash_table.hash = lambda k: self.hash2(k, inner_hash_table)
            self.top_level_table[k1] = inner_hash_table

        # if self.top_level_table.array[outer_pos] is None:
        #     raise KeyError(key)  # Key does not exist in the hash table

        # if self.top_level_table.array[outer_pos] is None:
        #    raise KeyError(key)  # Key does not exist in the hash table
        # if self.top_level_table.array[outer_pos][0] != k1:
        #    raise KeyError(key)

        # inner_hash_table = self.top_level_table.array[outer_pos][1]
        inner_hash_table = self.top_level_table[k1]
        try:
            inner_hash_table[k2]
        except KeyError:
            self.count += 1
        inner_hash_table[k2] = data

    def __delitem__(self, key: tuple[K1, K2]) -> None:

        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.

        :parameter: key: tuple[K1, K2]
        :complexity: O(m+n)
        """

        self.top_level_table.hash = self.hash1
        k1, k2 = key
        del self.top_level_table[k1][k2]
        if len(self.top_level_table[k1]) == 0:
            del self.top_level_table[k1]
        self.count -= 1

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)

        method:
        Create a new top-level hash table with increased size
        Reinsert all values into the new hash table
        """
        self.top_level_table.hash = self.hash1
        new_top_level_table = LinearProbeTable[K1, LinearProbeTable[K2, V]](sizes=self.TABLE_SIZES)

        for start in self.top_level_table.array:
            if start is not None:
                key1, inner_hash_table = start
                new_inner_hash_table = LinearProbeTable[K2, V](sizes=self.internal_sizes)
                new_inner_hash_table.hash = lambda k: self.hash2(k, new_inner_hash_table)

                for inner_start in inner_hash_table.array:
                    if inner_start is not None:
                        key2, value = inner_start
                        new_inner_hash_table[key2] = value

                new_top_level_table[key1] = new_inner_hash_table

        self.top_level_table = new_top_level_table
        # raise NotImplementedError()

    @property
    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)
        """
        return self.top_level_table.table_size

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        """
        return self.count
        # raise NotImplementedError()

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """

        raise NotImplementedError()
