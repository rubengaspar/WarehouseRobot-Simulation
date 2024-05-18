class GridManager:

    robots = []
    packages = []
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
        self.grid = [[None for _ in range(width)] for _ in range(height)]

    def add_goal(self, goal):
        """
        :param goal: The goal to be added.
        :type goal: Goal
        :return: None
        """

        if self.is_valid_position(goal.position):
            self.goals.append(goal)
            self.grid[goal.position[1]][goal.position[0]] = goal

    def add_robot(self, robot):
        """
        Add a robot to the grid at the robot's position.

        :param robot: The robot object to be added to the GridManager's robot list
        :type robot: Robot
        :return: None
        """
        if self.is_valid_position(robot.position):
            self.robots.append(robot)
            self.grid[robot.position[1]][robot.position[0]] = robot

    def add_package(self, package):
        """
        Add a package to the grid at the package's position.

        :param package: The package to be added to the grid.
        :type package: Package
        :return: None
        """
        if self.is_valid_position(package.position):
            self.packages.append(package)
            self.grid[package.position[1]][package.position[0]] = package

    def is_within_limits(self, position):
        """
        Check if the given position is occupied in the grid
        :param position: a tuple representing the (x, y) coordinates of the position
        :type position: tuple
        :return: True if the position is occupied, False otherwise
        :rtype: bool
        """
        x, y = position

        if 0 <= x < self.width and 0 <= y < self.height:
            return True
        return False

    def is_occupied(self, position):
        """
        Check if the given position is occupied in the grid
        :param position: a tuple representing the (x, y) coordinates of the position
        :type position: tuple
        :return: True if the position is occupied, False otherwise
        :rtype: bool
        """
        x, y = position

        if self.grid[y][x] is not None:
            return True
        return False

    def is_valid_position(self, position):
        """
        Check if the given position is valid within the limits of the grid.

        :param position: a tuple representing the (x, y) coordinates of the position
        :type position: tuple
        :return: True if the position is valid, False otherwise
        :rtype: bool
        """

        if not self.is_occupied(position) and self.is_within_limits(position):
            return True
        return False

    def reset(self):
        """
        Resets the grid, robots, and packages to their initial state.

        :return: None
        """
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.robots = []
        self.packages = []
        self.goals = []
