# goal.py
from src.package import Package
from src.position import Position


class Goal:
	color = "green"
	packages = []

	def __init__(self, id, position: 'Position'):
		self.id = id
		self.position = position
		self.delivered_packages = 0

	def deliver_package(self, package: 'Package'):
		self.packages.append(package)
		self.delivered_packages += 1
