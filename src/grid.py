# grid.py
import json

from src.cell import Cell
from src.goal import Goal
from src.package import Package
from src.position import Position
from src.robot import Status, Robot


class Grid:
	def __init__(self, width: int, height: int):
		self.goals = []
		self.goal_count = 0
		self.robots = []
		self.robot_count = 0
		self.packages = []
		self.package_count = 0

		self.width = width
		self.height = height

		# Generate grid
		self.grid = []
		for y in range(height):
			row = []
			for x in range(width):
				cell = Cell(Position(x, y))
				row.append(cell)

			self.grid.append(row)

	@classmethod
	def grid_from_json(cls, json_file: str):
		with open(f'./maps/{json_file}') as f:
			data = json.load(f)

		grid = cls(data['width'], data['height'])

		for item in data['cells']:

			position = Position(item['position']['x'], item['position']['y'])
			cell = Cell(position, item['max_load'])
			for connection in item['connections']:
				connection_position = Position(connection['to_cell']['x'], connection['to_cell']['y'])
				connection_cell = grid.get_cell(connection_position)
				cell.add_connection(connection_cell, connection['weight'])

			if item['robot'] is not None:
				robot = Robot.from_json(item['robot'])
				cell.add_robot(robot)

			if item['goal'] is not None:
				goal = Goal.from_json(item['goal'])
				cell.add_goal(goal)

			for package_data in item['packages']:
				package = Package.from_json(package_data)
				cell.add_package(package)

			grid.grid[item['position']['y']][item['position']['x']] = cell

		return grid

	def get_cell(self, position: Position):
		x, y = position.x, position.y
		return self.grid[y][x]

	def is_inside_grid(self, position: Position):
		x, y = position.x, position.y
		return 0 <= x < self.width and 0 <= y < self.height

	def is_valid_move(self, position: Position):
		return self.is_inside_grid(position) and not self.get_cell(position).has_robot()

	def move_robots(self):
		for row in self.grid:
			for cell in row:
				if cell.robot:
					old_position = cell.robot.position
					next_position = cell.robot.update_position(self)
					if next_position == old_position:
						cell.robot.change_status(Status.IDLE)
					else:
						cell.robot.change_status(Status.ACTIVE)
						next_cell = self.get_cell(next_position)
						if next_cell.has_package():
							# TODO: Load while robot has capacity
							cell.robot.load(package=next_cell.packages)
						elif next_cell.has_goal():
							cell.robot.unload(grid_manager=self)

	def add_robot(self, position: Position, robot: Robot):
		cell = self.get_cell(position)
		if not cell.has_robot():
			cell.add_robot(robot)
			self.robots.append(robot)
			self.robot_count += 1

	def remove_robot(self, position: Position):
		cell = self.get_cell(position)
		if cell.has_robot():
			cell.robot = None
			# lacks line to remove from grid's robot list
			self.robot_count -= 1

	def add_package(self, position: Position, package: Package):
		cell = self.get_cell(position)
		if cell.can_load_package():
			cell.add_package(package)
			self.packages.append(package)
			self.package_count += 1

	def remove_package(self, position: Position):
		cell = self.get_cell(position)
		if len(cell.packages) > 0:
			# TODO: add logic to pop item (FIFO)
			cell.package = None
			# lacks line to remove from grid's packages list
			self.package_count -= 1

	def add_goal(self, position: Position, goal: Goal):
		cell = self.get_cell(position)
		if not cell.has_goal():
			cell.add_goal(goal)
			self.goals.append(goal)
			self.goal_count += 1

	def remove_goal(self, position: Position):
		cell = self.get_cell(position)
		if cell.has_goal():
			cell.goal = None
			# lacks line to remove from grid's goal list
			self.goal_count -= 1

	def reset(self):
		for row in self.grid:
			for cell in row:
				cell.reset()
