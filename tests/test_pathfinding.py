import unittest
from unittest.mock import Mock
import sys
import os

# Modify the path to include the /src directory
sys.path.append(os.path.join(os.getcwd(), 'src'))
from pathfinding import Pathfinding


class TestPathfinding(unittest.TestCase):

	def setUp(self):
		self.pathfinding = Pathfinding(Mock())

	def test_a_star_path_found(self):
		start = (0, 0)
		goal = (2, 2)
		self.pathfinding.heuristic = Mock(return_value=1)
		self.pathfinding.get_neighbours = Mock(return_value=[(1, 1), (2, 2)])
		self.pathfinding.reconstruct_path = Mock(return_value=[(0, 0), (1, 1), (2, 2)])  # just a mock path
		result = self.pathfinding.a_star(start, goal)
		self.assertEqual(result, [(0, 0), (1, 1), (2, 2)])

	def test_a_star_no_path(self):
		start = (0, 0)
		goal = (3, 3)
		self.pathfinding.heuristic = Mock(return_value=sys.maxsize)
		self.pathfinding.get_neighbours = Mock(return_value=[(1, 1), (2, 2)])  # no way to (3, 3)
		result = self.pathfinding.a_star(start, goal)
		self.assertEqual(result, [])


if __name__ == "__main__":
	unittest.main()
