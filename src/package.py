class Package:
    """Initialize the package with a position.

    :param position: The position of the package.
    :type position: tuple(float, float)
    """
    color = "red"

    def __init__(self, id, position):
        """
        Constructor method for initializing an instance of the class.

        :param id: The identifier for the package.
        :type id: Any valid data type.
        :param position: The position parameter.
        :type position: tuple(float, float)
        """
        self.id = id
        self.position = position
        self.moving = False
        self.searchable = True

    def find_nearest_goal(self, goals):
        """
        Find the nearest goal from a given list of goals based on the current position of the package.

        :param goals: A list of goal objects.
        :type goals: list
        :return: The nearest goal object.
        :rtype: Goal
        """
        min_distance = float('inf')
        nearest_goal = None

        for goal in goals:
            distance = abs(self.position[0] - goal.position[0]) + abs(self.position[1] - goal.position[1])
            if distance < min_distance:
                nearest_goal = goal
                min_distance = distance

        return nearest_goal

    def find_nearest_package(self, packages):
        """
        Finds the nearest package from a given list of packages.

        :param packages: A list of package objects.
        :return: The nearest package object.
        """
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
