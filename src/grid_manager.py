class GridManager:
    def __init__(self, width, height):
        """
        Initialize a new instance of the class GridManager.

        :param width: The width of the grid.
        :type width: int
        :param height: The height of the grid.
        :type height: int
        """
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        self.robots = []
        self.packages = []

    def add_robot(self, robot):
        """
        Add a robot to the grid at the robot's position.

        :param robot: The robot object to be added to the GridManager's robot list
        :return: None
        """
        if self.is_valid_position(robot.position):
            self.robots.append(robot)
            self.grid[robot.position[1]][robot.position[0]] = robot

    def add_package(self, package):
        """
        Add a package to the grid at the package's position.

        :param package: The package to be added to the grid.
        :return: None
        """
        if self.is_valid_position(package.position):
            self.packages.append(package)
            self.grid[package.position[1]][package.position[0]] = package

    def move_robot(self, robot, new_position):
        """
        Moves the given robot to the new position on the grid.

        :param robot: The robot object to move.
        :param new_position: The new position to move the robot to.
        :return: None
        """
        if self.is_valid_position(new_position):
            self.grid[robot.position[1]][robot.position[0]] = None
            robot.position = new_position
            self.grid[new_position[1]][new_position[0]] = robot

    def is_valid_position(self, position):
        """
        Check if the given position is valid within the grid.

        :param position: a tuple representing the (x, y) coordinates of the position
        :type position: tuple
        :return: True if the position is valid, False otherwise
        :rtype: bool
        """
        x, y = position
        if 0 <= x < self.width and 0 <= y < self.height and self.grid[y][x] is None:
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
