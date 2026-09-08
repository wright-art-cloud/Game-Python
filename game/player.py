"""Player state and player actions."""

from game.resource import Resource


class Player:
	"""Represent a player who owns resources and units."""

	def __init__(self, name, resources=None):
		if not isinstance(name, str) or not name.strip():
			raise ValueError("Player name cannot be empty")

		self._name = name
		self._resources = resources or Resource()
		self._units = []

	@property
	def name(self):
		"""Return the player's name."""
		return self._name

	@property
	def resources(self):
		"""Return the player's resource manager."""
		return self._resources

	@property
	def units(self):
		"""Return the player's units without exposing the internal list."""
		return tuple(self._units)

	def add_unit(self, unit):
		"""Add a unit to the player's army."""
		self._units.append(unit)

	def remove_unit(self, unit):
		"""Remove a unit from the player's army."""
		self._units.remove(unit)

	def collect_resource(self, resource_type, amount):
		"""Add collected resources to the player's stockpile."""
		self._resources.add(resource_type, amount)

	def spend_resource(self, resource_type, amount):
		"""Spend resources from the player's stockpile."""
		self._resources.spend(resource_type, amount)