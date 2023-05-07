from __future__ import annotations

from typing import List

from mountain import Mountain

class MountainOrganiser:

    # def __init__(self) -> None:
    #     self.mountains = []
    #     # raise NotImplementedError()
    #
    # def cur_position(self, mountain: Mountain) -> int:
    #     index = self._binary_search(mountain)
    #     if index >= 0:
    #         return index
    #     else:
    #         raise KeyError(f"Mountain {mountain} not found")
    #     # raise NotImplementedError()
    #
    # def add_mountains(self, mountains: list[Mountain]) -> None:
    #     self.mountains.extend(mountains)
    #     self.mountains.sort(key=lambda m: (m.length, m.name))
    #     # raise NotImplementedError()
    #
    # def _binary_search(self, mountain: Mountain) -> int:
    #     left = 0
    #     right = len(self.mountains) - 1
    #
    #     while left <= right:
    #         mid = (left + right) // 2
    #         mid_mountain = self.mountains[mid]
    #
    #         if mid_mountain.length < mountain.length:
    #             left = mid + 1
    #         elif mid_mountain.length > mountain.length:
    #             right = mid - 1
    #         else:
    #             if mid_mountain.name < mountain.name:
    #                 left = mid + 1
    #             elif mid_mountain.name > mountain.name:
    #                 right = mid - 1
    #             else:
    #                 return mid
    #
    #     return -1


    def __init__(self) -> None:
        self.mountains: List[Mountain] = []

    def cur_position(self, mountain: Mountain) -> int:
        # Sort the mountains list by length and name
        # sorted_mountains = sorted(self.mountains, key=lambda m: (m.length, m.name))

        # Perform a binary search to find the position of the mountain
        left = 0
        right = len(self.mountains) - 1

        while left <= right:
            mid = (left + right) // 2
            if self.mountains[mid] == mountain:
                return mid
            elif self.mountains[mid] < mountain:
                left = mid + 1
            else:
                right = mid - 1

        raise KeyError("Mountain not found")

    def add_mountains(self, mountains: List[Mountain]) -> None:
        self.mountains.extend(mountains)
        self.mountains.sort(key=lambda m: (m.length, m.name))



