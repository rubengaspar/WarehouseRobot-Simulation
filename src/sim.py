# sim.py

from grid import GridManager
from gui import GUI


class Simulation:
	def __init__(self, grid_manager):
		self.grid_manager = grid_manager
		self.simulation_running = False

	def start_simulation(self):
		if len(self.grid_manager.goals) > 0 and len(self.grid_manager.packages) > 0 and len(
				self.grid_manager.robots) > 0:
			self.simulation_running = True
			self.update_simulation()
		else:
			print("Insufficient components to start simulation.")

	def stop_simulation(self):
		self.simulation_running = False

	def reset(self):
		self.grid_manager.reset()

	def update_simulation(self):
		if self.simulation_running:
			for row in self.grid_manager.grid:
				for cell in row:
					if cell.robot:
						cell.robot.calculate_path(self.grid_manager)

			self.grid_manager.move_robots()


# Example of running the simulation
if __name__ == "__main__":
	grid_manager = GridManager(width=15, height=15)
	simulation = Simulation(grid_manager)
	gui = GUI(grid_manager)

	# Bind simulation controls to the GUI (example only, more integration needed)
	gui.button_start.config(command=simulation.start_simulation)
	gui.button_pause.config(command=simulation.stop_simulation)
	gui.button_reset.config(command=simulation.reset)

	gui.run()
