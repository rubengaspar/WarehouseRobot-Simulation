class Package:
    """Initialize the package with a position.

    :param position: The position of the package.
    :type position: tuple(float, float)
    """
    color = "red"

    def __init__(self, id, position):
        """
            Constructor method for initializing an instance of the class.

            :param position: The position parameter.
            :type position: Any valid data type.
        """
        self.id = id
        self.position = position
