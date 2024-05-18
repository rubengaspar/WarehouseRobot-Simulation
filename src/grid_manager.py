
from robot import Robot, Status
from package import Package
from goal import Goal
class GridManager:

    robots = []
    packages = []
    packages_loaded = []
    goals = []

    def __init__(self, width, height):
        """
        Initialize an instance of the class with the given width and height.

        :param width: The width of the grid.
        :type width: int
        :param height: The height of the grid.
        :type height: int
        """
        self.width = width
        self.height = height
        self.grid = [[[] for _ in range(width)] for _ in range(height)]

    def move_robots(self):
        for robot in self.robots:
            print(f"[Robot id: {robot.id} Status Report")
            print(f"Robot at {robot.position}, current load: {len(robot.packages)}")
            next_position = robot.update_position(self)
            if next_position == robot.position:
                robot.change_status(Status.IDLE)
            else:
                robot.change_status(Status.ACTIVE)
                if self.is_occupied_by_package(next_position):
                    robot.load(package=self.get_package(next_position), grid_manager=self)
                    self.unload()
                elif self.is_occupied_by_goal(next_position):
                    robot.unload(grid_manager=self)


    def deliver_package_at_goal(self, package, position):
        # get the object(s) at the given position and check if any of them is a goal
        cell_contents = self.grid[position[1]][position[0]]
        for item in cell_contents:
            if isinstance(item, Goal):
                goal = item
                # deliver the package to the goal
                goal.deliver_package(package)
                return True
        return False

    def add_goal(self, goal):
        """
        :param goal: The goal to be added.
        :type goal: Goal
        :return: None
        """
        x, y = goal.position
        if self.is_valid_move(goal.position):
            self.goals.append(goal)
            self.grid[y][x].append(goal)

    def add_robot(self, robot):
        """
        Add a robot to the grid at the robot's position.

        :param robot: The robot object to be added to the GridManager's robot list
        :type robot: Robot
        :return: None
        """
        x, y = robot.position
        if self.is_valid_move(robot.position):
            self.robots.append(robot)
            self.grid[y][x].append(robot)

    def add_package(self, package):
        """
        Add a package to the grid at the package's position.

        :param package: The package to be added to the grid.
        :type package: Package
        :return: None
        """
        x, y = package.position
        if self.is_valid_move(package.position):
            self.packages.append(package)
            self.grid[y][x].append(package)

    def remove_package(self, package):
        """
        Remove the package from the grid and add it to packages_loaded list.

        :param package: The package to be loaded.
        :return: None
        """
        x, y = package.position
        if package in self.packages:
            self.packages.remove(package)
            self.packages_loaded.append(package)
            self.grid[y][x].remove(package)

    def get_package(self, position):
        x, y = position
        for item in self.grid[y][x]:
            if isinstance(item, Package):
                self.packages.remove(item)
                self.grid[y][x].remove(item)
                return item
        return None

    def is_within_limits(self, position):
        """
        Checks if the given position is within the limits of the object's width and height.

        :param position: A tuple representing the x and y coordinates of the position to check.
        :type position: tuple

        :return: True if the position is within the limits, False otherwise.
        :rtype: bool
        """
        x, y = position

        if 0 <= x < self.width and 0 <= y < self.height:
            return True
        return False

    def is_occupied_by_robot(self, position):
        """
        Check if the given position is occupied by a robot.

        :param position: A tuple representing the position of the grid (x, y).
        :return: True if the given position is occupied by a Robot object, False otherwise.
        """
        x, y = position
        items = self.grid[y][x]
        if items:
            for item in items:
                if isinstance(item, Robot):
                    return True
        return False

    def is_occupied_by_other_robot(self, position, robot):
        """
        Check if the given position is occupied by a robot.

        :param position: A tuple representing the position of the grid (x, y).
        :return: True if the given position is occupied by a Robot object, False otherwise.
        """
        x, y = position
        items = self.grid[y][x]
        if items:
            for item in items:
                if isinstance(item, Robot):
                    if item.id == robot.id:
                        return True
        return False

    def is_occupied_by_package(self, position):
        """
        Check if the specified position on the grid is occupied by a package.

        :param position: A tuple representing the position on the grid as (x, y).
        :type position: tuple
        :return: True if the position is occupied by a package, False otherwise.
        :rtype: bool
        """
        x, y = position
        items = self.grid[y][x]
        if items:
            for item in items:
                if isinstance(item, Package):
                    return True
        return False

    def is_occupied_by_goal(self, position):
        """
        Checks if the given position on the grid is occupied by a Goal object.

        :param position: A tuple representing the position on the grid. The first element is the x-coordinate and the second element is the y-coordinate.
        :type position: tuple

        :return: True if the position is occupied by a Goal object, False otherwise.
        :rtype: bool
        """
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
        """
        Clears the specified position on the grid.

        :param position: A tuple containing the x and y coordinates of the position.
        :return: None
        """
        x, y = position
        if self.grid[y][x] is None:
            print(f"Trying to clear a position on the grid that is: {self.grid[y][x]}")
        else:
            self.grid[y][x] = []


    def is_valid_move(self, position):
        """
        Check if the given position is valid within the limits of the grid.

        :param position: a tuple representing the (x, y) coordinates of the position
        :type position: tuple
        :return: True if the position is valid, False otherwise
        :rtype: bool
        """

        if not self.is_occupied_by_robot(position) and self.is_within_limits(position):
            return True
        return False

    def reset(self):
        """
        Resets the grid, robots, and packages to their initial state.

        :return: None
        """
        self.robots = []
        self.packages = []
        self.goals = []
        self.grid = [[[] for _ in range(self.width)] for _ in range(self.height)]


