class Goal:
	"""
	Initializes an instance of the class Goal
	"""
	color = "green"
	packages = []

	def __init__(self, id, position):
		"""
		Initialize a new instance of the class.

		:param id: The ID of the object.
		:param position: The position of the object.
		"""
		self.id = id
		self.position = position
		self.delivered_packages = 0

	def deliver_package(self, package):
		"""
		:param package: the package to be delivered
		:return: None
		"""
		self.packages.append(package)
		self.delivered_packages += 1
