from src.connection import Connection
from src.goal import Goal
from src.package import Package
from src.position import Position
from src.robot import Robot


class Cell:

    def __init__(self, position: Position, max_load=10):
        self.position = position
        self.connections = []
        self.robot = None
        self.goal = None
        self.max_load = max_load
        self.packages = []

    def add_connection(self, to_cell: 'Cell', weight=1):
        connection = Connection(self, to_cell, weight)
        self.connections.append(connection)

    def remove_connection(self, to_cell: 'Cell'):
        if self.connections:
            updated_connections = []
            for c in self.connections:
                if c.to_cell != to_cell:
                    updated_connections.append(c)

            self.connections = updated_connections
            return True
        return False

    def add_robot(self, robot: Robot):
        if not self.robot:
            self.robot = robot
            return True
        return False

    def add_package(self, package: Package):
        if len(self.packages) < self.max_load:
            self.packages.append(package)
            return True
        return False

    def remove_package(self, package: Package):
        if self.packages:
            updated_packages = []
            for p in self.packages:
                if p != package:
                    updated_packages.append(p)

            self.packages = updated_packages
            return True
        return False

    def add_goal(self, goal: Goal):
        if not self.goal:
            self.goal = goal
            return True
        return False

    def is_occupied_by_robot(self):
        return self.robot is not None

    def has_package(self):
        return self.packages is not None

    def is_occupied_by_goal(self):
        return self.goal is not None

    def reset(self):
        self.robot = None
        self.packages = []
        self.goal = None

    def __repr__(self):
        return f"Cell({self.position}, Robot: {self.robot}, Goal: {self.goal}, Package: {self.package})"
