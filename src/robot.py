class Robot:
    """Initialize the robot with an id and position.

    :param id: The id of the robot.
    :type id: int
    :param position: The position of the robot.
    :type position: tuple
    """
    def __init__(self, id, position):
        """
        Initializes a new instance of the object.

        :param id: The ID of the object.
        :type id: int
        :param position: The position of the object.
        :type position: str
        """
        self.id = id
        self.position = position

    def move(self, direction):
        """
        :param direction: The direction to move in. Valid values are 'up', 'down', 'left', or 'right'.
        :return: The new position after the move is made.

        This method takes a direction as input and returns the new position after the move is made. It uses a dictionary of directions to determine the change in x and y coordinates. If the
        * given direction is valid, it calculates the new position by adding the corresponding change in coordinates to the current position. If the given direction is not valid, it returns
        * the current position.

        Example usage:
            position = (0, 0)
            obj = MyClass(position)
            new_position = obj.move('up')

        """
        directions = {'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}
        if direction in directions:
            dx, dy = directions[direction]
            return (self.position[0] + dx, self.position[1] + dy)
        return self.position
