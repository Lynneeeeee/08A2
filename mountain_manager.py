import mountain_organiser
from mountain import Mountain

class MountainManager:

    def __init__(self) -> None:
        self.mountains = []

    def add_mountain(self, mountain: Mountain):
        '''
        Add a mountain to the manager
        :parameter: mountain: Mountain
        :complexity: O(1)
        '''
        self.mountains.append(mountain)

    def remove_mountain(self, mountain: Mountain):
        '''
        Remove a mountain from the manager
        :parameter: mountain: Mountain
        :complexity: O(1)
        '''
        self.mountains.remove(mountain)

    def edit_mountain(self, old: Mountain, new: Mountain):
        '''
        Remove the old mountain and add the new mountain.
        :parameter: mountain: Mountain
        :complexity: O(1)
        '''
        index = self.mountains.index(old)
        self.mountains[index] = new

    def mountains_with_difficulty(self, diff: int) -> list[Mountain]:
        '''
        Return a list of all mountains with this difficulty.
        :parameter: diff: int difficulty of mountain
        :complexity: O(N)
        '''
        filtered_mountains = [mountain for mountain in self.mountains if mountain.difficulty == diff]
        return filtered_mountains

    def group_by_difficulty(self) -> list[list[Mountain]]:
        '''
        Returns a list of lists of all mountains, grouped by and sorted by ascending difficulty.
        :complexity: O(N)
        '''
        sorted_mountains = sorted(self.mountains, key=lambda mountain: (mountain.difficulty, mountain.elevation))
        grouped_mountains = []
        current_group = []

        for mountain in sorted_mountains:
            if not current_group or mountain.difficulty != current_group[0].difficulty:
                if current_group:
                    grouped_mountains.append(current_group)
                current_group = [mountain]
            else:
                current_group.append(mountain)

        if current_group:
            grouped_mountains.append(current_group)

        return grouped_mountains
