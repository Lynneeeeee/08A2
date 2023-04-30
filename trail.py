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
        # raise NotImplementedError()

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
        # raise NotImplementedError()

    def add_mountain_before(self, mountain: Mountain) -> TrailStore:
        """
        O(1)
        Adds a mountain in series before the current one.
        parameter: mountain
        return: TrailStore
        """
        new_series = TrailSeries(mountain, Trail(self))
        return new_series

        # raise NotImplementedError()

    def add_empty_branch_before(self) -> TrailStore:
        """
        O(1)
        Adds an empty branch, where the current trailstore is now the following path.
        return: TrailStore
        """
        new_split = TrailSplit(Trail(None), Trail(None), Trail(self))
        return new_split
        # raise NotImplementedError()

    def add_mountain_after(self, mountain: Mountain) -> TrailStore:
        """
        O(1)
        Adds a mountain after the current mountain, but before the following trail.
        parameter: mountain
        return TrailStore
        """
        new_mountain = mountain
        new_following = Trail(TrailSeries(new_mountain, self.following))
        new_series = TrailSeries(self.mountain, new_following)
        return new_series
        # raise NotImplementedError()

    def add_empty_branch_after(self) -> TrailStore:
        """
        O(1)
        Adds an empty branch after the current mountain, but before the following trail.
        return: TrailStore
        """
        new_following = Trail(TrailSplit(Trail(None), Trail(None), self.following))
        new_trail = TrailSeries(self.mountain, new_following)
        return new_trail
        # raise NotImplementedError()

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
        new_trail = Trail(TrailSeries(mountain, self))
        return new_trail
        # raise NotImplementedError()

    def add_empty_branch_before(self) -> Trail:
        """
        O(1)
        Adds an empty branch before everything currently in the trail.
        return: Trail
        """
        new_trail = Trail(TrailSplit(Trail(None), Trail(None), self))
        return new_trail
        # raise NotImplementedError()

    def follow_path(self, personality: WalkerPersonality) -> None:
        """
        Follow a path and add mountains according to a personality."""
        # raise NotImplementedError()

    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail."""
        raise NotImplementedError()

    def length_k_paths(self, k) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        """
        Returns a list of all paths of containing exactly k mountains.
        Paths are represented as lists of mountains.

        Paths are unique if they take a different branch, even if this results in the same set of mountains.
        """
        raise NotImplementedError()
