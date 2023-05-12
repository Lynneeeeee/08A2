from __future__ import annotations
from dataclasses import dataclass

from mountain import Mountain

from typing import TYPE_CHECKING, Union

# Avoid circular imports for typing.
if TYPE_CHECKING:
    from personality import WalkerPersonality

@dataclass
class TrailSplit:
    """
    A split in the trail.
       ___path_top____
      /               \
    -<                 >-path_follow-
      \__path_bottom__/
    """

    path_top: Trail
    path_bottom: Trail
    path_follow: Trail

    def remove_branch(self) -> TrailStore:
        """
        O(1)
        Removes the branch, should just leave the remaining following trail.
        return: TrailStore
        """
        return self.path_follow.store

@dataclass
class TrailSeries:
    """
    A mountain, followed by the rest of the trail

    --mountain--following--

    """

    mountain: Mountain
    following: Trail

    def remove_mountain(self) -> TrailStore:
        """
        O(1)
        Removes the mountain at the beginning of this series.
        return: TrailStore
        """
        return self.following.store

    def add_mountain_before(self, mountain: Mountain) -> TrailStore:
        """
        O(1)
        Adds a mountain in series before the current one.
        parameter: mountain
        return: TrailStore
        """
        return TrailSeries(mountain, Trail(self))

    def add_empty_branch_before(self) -> TrailStore:
        """
        O(1)
        Adds an empty branch, where the current trailstore is now the following path.
        return: TrailStore
        """
        return TrailSplit(Trail(None), Trail(None), Trail(self))

    def add_mountain_after(self, mountain: Mountain) -> TrailStore:
        """
        O(1)
        Adds a mountain after the current mountain, but before the following trail.
        parameter: mountain
        return TrailStore
        """
        return TrailSeries(self.mountain, Trail(TrailSeries(mountain, self.following)))

    def add_empty_branch_after(self) -> TrailStore:
        """
        O(1)
        Adds an empty branch after the current mountain, but before the following trail.
        return: TrailStore
        """
        return TrailSeries(self.mountain, Trail(TrailSplit(Trail(None), Trail(None), self.following)))

TrailStore = Union[TrailSplit, TrailSeries, None]

@dataclass
class Trail:

    store: TrailStore = None

    def add_mountain_before(self, mountain: Mountain) -> Trail:
        """
        O(1)
        Adds a mountain before everything currently in the trail.
        Parameter: mountain
        return: Trail
        """
        return Trail(TrailSeries(mountain, self))

    def add_empty_branch_before(self) -> Trail:
        """
        O(1)
        Adds an empty branch before everything currently in the trail.
        return: Trail
        """
        return Trail(TrailSplit(Trail(None), Trail(None), self))

    def follow_path(self, personality: WalkerPersonality) -> None:
        """
        O(n)

        Follow a path and add mountains according to a personality.

        method: Using the stack to store the trail, iterate the stack use the while loopt he trail which has been poped
        is represented the current trail to be processed. If the current trail have the mountain, use add_mountain
        method the record the mountain into the walker's list of visited mountains. If current trail have a split path,
        use select_branch to decide which path to take. If the current trail has only a top or bottom path, append the
        existing path to the stack.

        parameter: personality
        """
        stack = [self]
        while stack:
            current_trail = stack.pop()
            # print(f"Current trail: {current_trail}, Stack: {stack}")

            if current_trail:
                if type(current_trail.store) == TrailSeries:
                    personality.add_mountain(current_trail.store.mountain)
                    stack.append(current_trail.store.following)

                elif type(current_trail.store) == TrailSplit:
                    if personality.select_branch(current_trail.store.path_top, current_trail.store.path_bottom):
                        stack.append(current_trail.store.path_follow)
                        stack.append(current_trail.store.path_top)
                    else:
                        stack.append(current_trail.store.path_follow)
                        stack.append(current_trail.store.path_bottom)

    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail."""
        mountains = []
        stack = [self]

        while stack:
            current_trail = stack.pop()

            if current_trail:
                if isinstance(current_trail.store, TrailSeries):
                    mountains.append(current_trail.store.mountain)
                    stack.append(current_trail.store.following)
                elif isinstance(current_trail.store, TrailSplit):
                    stack.append(current_trail.store.path_top)
                    stack.append(current_trail.store.path_bottom)
                    stack.append(current_trail.store.path_follow)

        return mountains[::-1] if mountains else []

    def length_k_paths(self, k) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        """
        Returns a list of all paths of containing exactly k mountains.
        Paths are represented as lists of mountains.

        Paths are unique if they take a different branch, even if this results in the same set of mountains.
        """
        return [ i for i in self.get_all_paths() if len(i)==k ]

    def get_all_paths(self) -> list[list[Mountain]]:
        if self.store is None:
            return [[]]

        if isinstance(self.store,TrailSplit):
            retval=[]
            for i in self.store.path_top.get_all_paths()+self.store.path_bottom.get_all_paths():
                for j in self.store.path_follow.get_all_paths():
                    retval.append(i+j)
            return retval

        if isinstance(self.store, TrailSeries):
            return [[self.store.mountain] + i for i in self.store.following.get_all_paths()]