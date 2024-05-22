# package.py
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.position import Position
    from src.goal import Goal


class Package:
    color = "red"

    def __init__(self, id, position: 'Position'):
        self.id = id
        self.position = position
        self.moving = False
        self.searchable = True

    def find_nearest_goal(self, goals: List['Goal']):
        min_distance = float('inf')
        nearest_goal = None

        for goal in goals:
            distance = abs(self.position[0] - goal.position[0]) + abs(self.position[1] - goal.position[1])
            if distance < min_distance:
                nearest_goal = goal
                min_distance = distance

        return nearest_goal

    def find_nearest_package(self, packages: List['Package']):
        nearest_package = None
        min_distance = float('inf')
        if packages:
            for package in packages:
                if package.searchable:
                    distance = abs(self.position[0] - package.position[0]) + abs(self.position[1] - package.position[1])

                    if distance < min_distance:
                        nearest_package = package
                        min_distance = distance

            return nearest_package
        else:
            return None
