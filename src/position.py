# position.py

class Position:
	def __init__(self, x: int, y: int):
		self.x = x
		self.y = y

	def __repr__(self):
		return f"Position({self.x}, {self.y})"