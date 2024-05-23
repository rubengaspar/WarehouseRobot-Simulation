# sim.py

from gui import GUI
from src.grid import Grid


class Simulation:
	def __init__(self, grid: Grid):
		self.grid = grid
		self.simulation_running = False

	def start_simulation(self):
		if len(self.grid.goals) > 0 and len(self.grid.packages) > 0 and len(self.grid.robots) > 0:
			self.simulation_running = True
			self.update_simulation()
		else:
			print("Insufficient components to start simulation.")

	def stop_simulation(self):
		self.simulation_running = False

	def reset(self):
		self.grid.reset()

	def update_simulation(self):
		if self.simulation_running:
			for row in self.grid.grid:
				for cell in row:
					if cell.robot:
						cell.robot.calculate_path(self.grid)

			self.grid.move_robots()
