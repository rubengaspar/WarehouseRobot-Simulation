
from robot import Robot, Status
from package import Package
from goal import Goal
class GridManager:

    robots = []
    packages = []
    packages_loaded = []
    goals = []

    def __init__(self, width, height):

        self.width = width
        self.height = height
        self.grid = [[[] for _ in range(width)] for _ in range(height)]

    def move_robots(self):
        for robot in self.robots:
            print(f"[Robot id: {robot.id} at {robot.position}, current load: {len(robot.packages)}")
            old_position = robot.position
            next_position = robot.update_position(self)
            if next_position == old_position:
                robot.change_status(Status.IDLE)
            else:
                robot.change_status(Status.ACTIVE)
                if self.is_occupied_by_package(next_position):
                    robot.load(package=self.get_package(next_position))
                elif self.is_occupied_by_goal(next_position):
                    robot.unload(grid_manager=self)

    def add_goal(self, goal):

        x, y = goal.position
        if self.is_valid_move(goal.position):
            self.goals.append(goal)
            self.grid[y][x].append(goal)

    def add_robot(self, robot):

        x, y = robot.position
        if self.is_valid_move(robot.position):
            self.robots.append(robot)
            self.grid[y][x].append(robot)

    def add_package(self, package):

        x, y = package.position
        if self.is_valid_move(package.position):
            self.packages.append(package)
            self.grid[y][x].append(package)

    def deliver_package_at_goal(self, package, position):
        # get the object(s) at the given position and check if any of them is a goal
        x, y = position
        cell_contents = self.grid[y][x]
        for item in cell_contents:
            if isinstance(item, Goal):
                goal = item
                # deliver the package to the goal
                goal.deliver_package(package)
                return True
        return False

    def get_package(self, position):
        x, y = position
        for item in self.grid[y][x]:
            if isinstance(item, Package):
                self.packages.remove(item)
                self.grid[y][x].remove(item)
                return item
        return None

    def is_within_limits(self, position):

        x, y = position

        if 0 <= x < self.width and 0 <= y < self.height:
            return True
        return False

    def is_occupied_by_robot(self, position):

        x, y = position
        items = self.grid[y][x]
        if items:
            for item in items:
                if isinstance(item, Robot):
                    return True
        return False

    def is_occupied_by_other_robot(self, position, robot):

        x, y = position
        items = self.grid[y][x]
        if items:
            for item in items:
                if isinstance(item, Robot):
                    if item.id == robot.id:
                        return True
        return False

    def is_occupied_by_package(self, position):

        x, y = position
        items = self.grid[y][x]
        if items:
            for item in items:
                if isinstance(item, Package):
                    return True
        return False

    def is_occupied_by_goal(self, position):

        x, y = position
        items = self.grid[y][x]
        if items:
            for item in items:
                if isinstance(item, Goal):
                    return True
        return False

    def get_object(self, position):
        x, y = position
        return self.grid[y][x]

    def clear_position(self, position):

        x, y = position
        if self.grid[y][x] is None:
            print(f"Trying to clear a position on the grid that is: {self.grid[y][x]}")
        else:
            self.grid[y][x] = []


    def is_valid_move(self, position):

        if not self.is_occupied_by_robot(position) and self.is_within_limits(position):
            return True
        return False

    def reset(self):

        self.robots = []
        self.packages = []
        self.goals = []
        self.grid = [[[] for _ in range(self.width)] for _ in range(self.height)]


