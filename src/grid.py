# grid.py
import json

from src.cell import Cell
from src.goal import Goal
from src.package import Package
from src.position import Position
from src.robot import Status, Robot

class Grid:
	def __init__(self, width: int, height: int):
		self.goal_count = 0
		self.robot_count = 0
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
	def from_json(cls, json_file: str):
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

	def get_cell(self, position):
		x, y = position
		return self.grid[y][x]

	def is_within_limits(self, position: Position):
		x, y = position
		return 0 <= x < self.width and 0 <= y < self.height

	def is_valid_move(self, position: Position):
		return self.is_within_limits(position) and not self.get_cell(position).is_occupied_by_robot()

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
							cell.robot.load(package=next_cell.package)
						elif next_cell.is_occupied_by_goal():
							cell.robot.unload(grid_manager=self)

	def add_robot(self, position: Position, robot: Robot):
		cell = self.get_cell(position)
		if not cell.is_occupied_by_robot():
			cell.add_robot(robot)
			self.robot_count += 1

	def remove_robot(self, position: Position):
		cell = self.get_cell(position)
		if cell.is_occupied_by_robot():
			cell.robot = None
			self.robot_count -= 1

	def add_package(self, position: Position, package: Package):
		cell = self.get_cell(position)
		if not cell.has_package():
			cell.add_package(package)
			self.package_count += 1

	def remove_package(self, position: Position):
		cell = self.get_cell(position)
		if cell.has_package():
			cell.package = None
			self.package_count -= 1

	def add_goal(self, position: Position, goal: Goal):
		cell = self.get_cell(position)
		if cell.is_occupied_by_goal():
			cell.add_goal(goal)
			self.goal_count += 1

	def remove_goal(self, position: Position):
		cell = self.get_cell(position)
		if cell.is_occupied_by_goal():
			cell.goal = None
			self.goal_count -= 1

	def reset(self):
		for row in self.grid:
			for cell in row:
				cell.reset()
