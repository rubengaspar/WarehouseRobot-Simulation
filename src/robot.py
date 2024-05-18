class Robot:
    """
    :class:`Robot`

    This class represents a robot object with various properties and methods.

    Attributes:
        color (str): The color of the robot (default: 'blue').
        id (any): The unique identifier for the robot.
        position (tuple(float, float)): The current position of the robot.
        goal: The goal position for the robot.
        path: The calculated path from the current position to the goal.

    Methods:
        __init__(self, id, position)
            This method is the constructor for the class. Initializes the robot with the given id and position.

        set_goal(self, goal)
            Sets the given goal as the new value for the `goal` attribute.

        calculate_path(self, pathfinder, grid_manager)
            Calculates the path from the current position to the goal using the A* algorithm.

        update_position(self, grid_manager)
            Updates the position of the robot based on the given grid_manager.

        find_nearest_package(self, packages)
            Finds the nearest package from a given list of packages.

        find_nearest_goal(self, goals)
            Finds the nearest goal from a list of goals.
    """
    color = 'blue'

    def __init__(self, id, position):
        """
        This method is the constructor for the class.

        :param id: The unique identifier for the object.
        :type id: any
        :param position: The current position of the object.
        :type position: tuple(float, float)

        :return: None
        """
        self.id = id
        self.position = position
        self.goal = None
        self.path = []

    def set_goal(self, goal):
        """
        :param goal: The goal to be set as the new value for the goal attribute.
        :return: None
        """
        self.goal = goal

    def calculate_path(self, pathfinder, grid_manager):
        """
        Calculate the path from the current position to the goal using A* algorithm.

        :param pathfinder: An instance of the pathfinding class that provides the A* algorithm implementation.
        :param grid_manager: An instance of the grid manager class that manages the grid and obstacles.
        :return: None

        """
        if self.goal:
            self.path = pathfinder.a_star(self.position, self.goal)

    def update_position(self, grid_manager):
        """
        :param grid_manager: An instance of the GridManager class that manages the positions in the grid.
        :return: None

        This method updates the position of the robot based on the given grid_manager. It checks if the current
        object has a path assigned to it. If it does, it removes the first position from * the path and assigns it to
        the variable 'next_position'. Then, it checks if the 'next_position' is a valid position using the
        'is_valid_position' method of the grid_manager. If it * is valid, it moves the robot to that position using
        the 'move_robot' method of the grid_manager. If the 'next_position' is not a valid position, it resets the
        path by assigning an * empty list to the 'path' attribute of the current object, which indicates that the
        path is blocked and needs to be recalculated.
        """
        if self.path:
            next_position = self.path.pop(0)
            if grid_manager.is_valid_position(next_position):
                grid_manager.move_robot(self, next_position)
            else:
                self.path = []  # Recalculate path if blocked

    def find_nearest_package(self, packages):
        """
        Finds the nearest package from a given list of packages.

        :param packages: A list of package objects.
        :return: The nearest package object.
        """
        nearest_package = None
        min_distance = float('inf')
        for package in packages:
            distance = abs(self.position[0] - package.position[0]) + abs(self.position[1] - package.position[1])
            if distance < min_distance:
                nearest_package = package
                min_distance = distance
        return nearest_package

    def find_nearest_goal(self, goals):
        """
        Find the nearest goal from a list of goals.

        :param goals: A list of goals represented as coordinate pairs [x, y].
        :return: The nearest goal from the list of goals.
        """
        nearest_goal = None
        min_distance = float('inf')
        for goal in goals:
            distance = abs(self.position[0] - goal[0]) + abs(self.position[1] - goal[1])
            if distance < min_distance:
                nearest_goal = goal
                min_distance = distance
        return nearest_goal
