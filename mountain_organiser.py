from __future__ import annotations

from typing import List

from mountain import Mountain

class MountainOrganiser:
    def __init__(self) -> None:
        self.mountains = []

    def add_mountains(self, mountains: List[Mountain]) -> None:
        """
        adding the mountain information to the mountains list
        sort the mountains list, this operation has O(NlogN) complexity

        :parameter: mountains: List[Mountain]
        :complexity: O(M + NlogN)
        """
        for mountain in mountains:
            self.mountains.append((mountain.length, mountain.name, mountain))

        self.mountains.sort()

    def _binary_search(self, mountains, target):
        """
        comparing the target value with the middle element of the list
        If they are not equal:
        the half in which the target cannot lie is eliminated
        the search continues on the remaining half
        again taking the middle element to compare to the target
        and repeating this until the target is found or the search space is reduced to zero

        :parameter: mountains, target
        :complexity: O(logN), where N is the length of the list mountains.
        """
        start, end = 0, len(mountains) - 1
        while start <= end:
            mid = (start + end) // 2
            if mountains[mid] == target:
                return mid
            elif mountains[mid] < target:
                start = mid + 1
            else:
                end = mid - 1
        return -1

    def cur_position(self, mountain: Mountain) -> int:
        """
        The binary search is to divides the search space in half until the target is found
        or the search space is exhausted
        and then If i != -1, the mountain was found in the list, and the method returns i.
        Otherwise, it raises a KeyError indicating that the mountain was not found in the list.

        :parameter: mountain
        :complexity: O(logN), where N is the total number of mountains included so far.
        """
        i = self._binary_search(self.mountains, (mountain.length, mountain.name, mountain))
        if i != -1:
            return i
        else:
            raise KeyError



