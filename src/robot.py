from enum import Enum
import time

from src.pathfinding import Pathfinding


class Status(Enum):
    OFF = "off"
    IDLE = "idle"
    ACTIVE = "active"

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
    packages = []
    path = []
    MAX_PACKAGES = 5
    MAX_WAIT = 10

    def __init__(self, id, position, max_packages=1):
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
        self.wait_times = 0
        self.status = Status.IDLE
        self.idle_time = 0
        self.active_time = 0
        self.off_time = 0
        self.waiting_time = 0
        self.time_status_changed = time.time()

    def calculate_path(self, grid_manager):
        if not self.path:
            print(f"Calculating new path for robot {self.id}")
            nearest_package = self.find_nearest_package(grid_manager.packages)
            if nearest_package:
                nearest_goal_from_package = nearest_package.find_nearest_goal_from_package(grid_manager.goals)
                nodes_to_visit = [self, nearest_package, nearest_goal_from_package]
                total_path = []

                for i in range(len(nodes_to_visit) - 1):
                    start = nodes_to_visit[i].position
                    goal = nodes_to_visit[i + 1].position
                    path = Pathfinding(grid_manager).a_star(start, goal)
                    total_path.extend(path[1:])

                self.add_to_path(total_path)
                print(f"Robot {self.id}'s path: {self.path}")

    def load(self, package):
        if len(self.packages) >= self.MAX_PACKAGES:
            print("Can't Load")
        else:
            self.packages.append(package)
            package.moving = True
            package.searchable = False

    def unload(self, grid_manager):
        if self.packages:
            # check if unload position is a goal or not
            if grid_manager.is_occupied_by_goal(self.position):
                # Unload packages to the goal
                for package in self.packages:
                    #TODO for later: Add logic for package to have specific destination goal to be checked
                    package.moving = False
                    grid_manager.deliver_package_at_goal(package, self.position)
                self.packages.clear()  # all packages have been delivered, clear the list
            else:
                # Drop packages to the grid
                for package in self.packages:
                    package.position = self.position
                    package.moving = False
                    package.searchable = True
                    grid_manager.add_package(package)
                self.packages.clear()  # all packages have been dropped, clear the list
        return True

    def add_to_path(self, path_to_add):
        self.path.extend(path_to_add)

    def update_position(self, grid_manager):
        """
        Updates the position of the robot on the grid.

        :param grid_manager: The grid manager object.
        :return: The new position of the robot.
        """
        if len(self.path) > 0:
            next_position = self.path[0]
            if grid_manager.is_valid_move(next_position):

                if grid_manager.is_occupied_by_other_robot(position=next_position, robot=self):
                    self.change_status(Status.IDLE)
                    #Next step occupied by robot, waiting
                    if self.wait_times > self.MAX_WAIT:
                        print(f"[Robot-{self.id}] I've been waiting for too long bitch, i'll get angry")
                        self.wait_times = 0
                        self.color = "magenta"

                    print(f"[Robot-{self.id}] Waiting... {self.wait_times}/{self.MAX_WAIT}")

                    self.wait_times += 1
                    return self.position
                else:
                    self.change_status(Status.ACTIVE)
                    x, y = self.position

                    if self.position == next_position:
                        self.change_status(Status.IDLE)
                        return self.position
                    else:
                        #Remove previous position by setting it to None
                        grid_manager.grid[self.position[1]][self.position[0]].remove(self)

                        #Remove position from path
                        self.position = next_position
                        self.path.pop(0)

                        #Place self at new position in grid manager's grid
                        grid_manager.grid[next_position[1]][next_position[0]].append(self)
                        self.wait_times = 0
                        return next_position
            else:
                self.path = []
                return self.position
        else:
            self.change_status(Status.IDLE)
            return self.position


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

    def change_status(self, new_status: Status):
        if not isinstance(new_status, Status):
            print(f"Invalid new status. Must be an instance of Status")
            return

        if new_status == self.status:
            return

        time_in_current_status = time.time() - self.time_status_changed

        if self.status == Status.IDLE:
            self.idle_time += time_in_current_status
        elif self.status == Status.ACTIVE:
            self.active_time += time_in_current_status
        elif self.status == Status.OFF:
            self.off_time += time_in_current_status

        self.status = new_status
        self.time_status_changed = time.time()

    def get_status_time(self, status: Status):
        """
        This method returns the time of the specified status
        :return: The time of the status
        :rtype: float
        """

        if not isinstance(status, Status):
            print("Invalid status. Must be an instance of Status enum.")
            return

        if self.status == status:
            return {
                Status.IDLE: self.idle_time + time.time() - self.time_status_changed,
                Status.ACTIVE: self.active_time + time.time() - self.time_status_changed,
                Status.OFF: self.off_time + time.time() - self.time_status_changed,
            }[status]

        return {
            Status.IDLE: self.idle_time,
            Status.ACTIVE: self.active_time,
            Status.OFF: self.off_time,
        }[status]
