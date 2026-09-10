"""Resource types and resource management."""


class Resource:
	"""Store and validate a player's gold, food, and wood."""

	RESOURCE_TYPES = ("gold", "food", "wood")

	def __init__(self, gold=0, food=0, wood=0):
		self._amounts = {
			"gold": gold,
			"food": food,
			"wood": wood,
		}
		self._validate_amounts()

	def get(self, resource_type):
		"""Return the amount of one resource type."""
		self._validate_type(resource_type)
		return self._amounts[resource_type]

	def add(self, resource_type, amount):
		"""Increase a resource amount."""
		self._validate_type(resource_type)
		self._validate_amount(amount)
		self._amounts[resource_type] += amount

	def spend(self, resource_type, amount):
		"""Decrease a resource amount when enough is available."""
		self._validate_type(resource_type)
		self._validate_amount(amount)

		if amount > self._amounts[resource_type]:
			raise ValueError("Insufficient resources")

		self._amounts[resource_type] -= amount

	def as_dict(self):
		"""Return a copy suitable for display or JSON serialization."""
		return self._amounts.copy()

	def _validate_amounts(self):
		for amount in self._amounts.values():
			self._validate_amount(amount)

	def _validate_type(self, resource_type):
		if resource_type not in self.RESOURCE_TYPES:
			raise ValueError(f"Unknown resource type: {resource_type}")

	@staticmethod
	def _validate_amount(amount):
		if not isinstance(amount, int) or isinstance(amount, bool):
			raise TypeError("Resource amounts must be integers")
		if amount < 0:
			raise ValueError("Resource amounts cannot be negative")