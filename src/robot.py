# robot.py
import math
from enum import Enum
import time
from typing import TYPE_CHECKING

from src.pathfinding import Pathfinding

if TYPE_CHECKING:
    from src.position import Position
    from src.goal import Goal


class Status(Enum):
    """
    Enumeration class representing the possible status values.

    :cvar OFF: Represents the "off" status.
    :cvar ACTIVE: Represents the "active" status.
    :cvar IDLE: Represents the "idle" status.
    :cvar BLOCKED: Represents the "blocked" status, unable to move due to obstacles.
    """
    OFF = "off"
    ACTIVE = "active"
    IDLE = "idle"
    BLOCKED = "blocked"


class Robot:
    color = 'blue'
    packages = []
    path = []

    def __init__(self, id, position, max_packages=5, max_blocked_times=10):

        self.id = id
        self.position = position

        self.max_packages = max_packages
        self.blocked_times = 0
        self.max_blocked_times = max_blocked_times

        self.status = Status.IDLE
        self.off_time = 0
        self.active_time = 0
        self.idle_time = 0

        self.blocked_time = 0
        self.time_status_changed = time.time()

    # TODO: Think if it is needed to change Pathing Logic?
    def calculate_path(self, grid):
        if not self.path:
            print(f"Calculating new path for robot {self.id}")
            nearest_package = self.find_nearest_package(grid.packages)

            if nearest_package:
                checkpoints = [self, nearest_package]

                while True:
                    last_visited = checkpoints[-1]
                    nearest_package_from_last_visited = last_visited.find_nearest_package(grid.packages)
                    nearest_goal_from_last_visited = last_visited.find_nearest_goal(grid.goals)
                    if nearest_goal_from_last_visited.position.distance_to(
                            last_visited.position) < nearest_package_from_last_visited.position.distance_to(
                            last_visited.position):
                        checkpoints.append(nearest_goal_from_last_visited)
                        break
                    else:
                        checkpoints.append(nearest_package_from_last_visited)

                total_path = []
                for i in range(len(checkpoints) - 1):
                    start = checkpoints[i].position
                    goal = checkpoints[i + 1].position
                    path = Pathfinding(grid).a_star(start, goal)
                    total_path.extend(path[1:])

                self.add_to_path(total_path)
                print(f"Robot {self.id}'s path: {self.path}")
            else:
                print("No packages found")
        else:
            print(f"Robot {self.id} already has a path")

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
            if grid_manager.has_goal(self.position):
                # Unload packages to the goal
                for package in self.packages:
                    #TODO: [for later] Add logic for package to have specific destination goal to be checked
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

    def update_position(self, grid):
        if len(self.path) > 0:
            next_position = self.path[0]
            if grid.is_valid_move(next_position):
                if grid.is_occupied_by_other_robot(position=next_position, robot=self):
                    self.change_status(Status.IDLE)
                    #Next step occupied by robot, waiting
                    if self.blocked_times > self.max_blocked_times:
                        print(f"[Robot-{self.id}] I've been waiting for too long bitch, i'll get angry")
                        self.blocked_times = 0
                        self.color = "magenta"

                    print(f"[Robot-{self.id}] Waiting... {self.blocked_times}/{self.max_blocked_times}")

                    self.blocked_times += 1
                    return self.position
                else:
                    self.change_status(Status.ACTIVE)
                    x, y = self.position.x, self.position.y

                    if self.position == next_position:
                        self.change_status(Status.IDLE)
                        return self.position
                    else:
                        #Remove previous position by setting it to None
                        grid.grid[self.position[1]][self.position[0]].remove(self)

                        #Remove position from path
                        self.position = next_position
                        self.path.pop(0)

                        #Place self at new position in grid manager's grid
                        grid.grid[next_position[1]][next_position[0]].append(self)
                        self.blocked_times = 0
                        return next_position
            else:
                self.path = []
                return self.position
        else:
            self.change_status(Status.IDLE)
            return self.position

    def find_nearest_package(self, packages):
        nearest_package = None
        min_distance = float('inf')
        if packages:
            for package in packages:
                if package.searchable:
                    # size of the vector between two points
                    distance = math.sqrt(abs(self.position.x - package.position.x) +
                                         abs(self.position.y - package.position.y))

                    if distance < min_distance:
                        nearest_package = package
                        min_distance = distance

            return nearest_package
        else:
            return None

    def find_nearest_goal(self, goals):
        nearest_goal = None
        min_distance = float('inf')
        for goal in goals:
            distance = math.sqrt(abs(self.position.x - goal.position.x) +
                                 abs(self.position.y - goal.position.y))
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
        elif self.status == Status.BLOCKED:
            self.blocked_time += time_in_current_status

        self.status = new_status
        self.time_status_changed = time.time()

    def get_status_time(self, status: Status):
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
