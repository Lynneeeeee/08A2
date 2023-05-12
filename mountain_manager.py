import mountain_organiser
from mountain import Mountain

class MountainManager:

    def __init__(self) -> None:
        self.mountains = []

    def add_mountain(self, mountain: Mountain):
        self.mountains.append(mountain)

    def remove_mountain(self, mountain: Mountain):
        self.mountains.remove(mountain)

    def edit_mountain(self, old: Mountain, new: Mountain):
        index = self.mountains.index(old)
        self.mountains[index] = new

    def mountains_with_difficulty(self, diff: int):
        filtered_mountains = [mountain for mountain in self.mountains if mountain.difficulty == diff]
        return filtered_mountains

    def group_by_difficulty(self) -> list[list[Mountain]]:
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
