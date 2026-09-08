"""Grid map and map-related operations."""


class Map:
	"""Represent a rectangular grid and the units occupying it."""

	def __init__(self, width=10, height=10):
		self._validate_dimension(width, "Width")
		self._validate_dimension(height, "Height")

		self._width = width
		self._height = height
		self._units = {}

	@property
	def width(self):
		"""Return the number of columns in the map."""
		return self._width

	@property
	def height(self):
		"""Return the number of rows in the map."""
		return self._height

	@property
	def units(self):
		"""Return all units currently placed on the map."""
		return tuple(self._units.values())

	def is_within_bounds(self, position):
		"""Return whether a position is a valid map coordinate."""
		if not self._is_position(position):
			return False

		x_coordinate, y_coordinate = position
		return 0 <= x_coordinate < self._width and 0 <= y_coordinate < self._height

	def is_occupied(self, position):
		"""Return whether a unit occupies a position."""
		return position in self._units

	def get_unit_at(self, position):
		"""Return the unit at a position, or None when it is empty."""
		return self._units.get(position)

	def add_unit(self, unit):
		"""Place a unit on the map."""
		if not self.is_within_bounds(unit.position):
			raise ValueError("Unit position is outside the map")
		if self.is_occupied(unit.position):
			raise ValueError("Map position is already occupied")
		if unit in self._units.values():
			raise ValueError("Unit is already on the map")

		self._units[unit.position] = unit

	def remove_unit(self, unit):
		"""Remove a unit from the map."""
		if unit.position not in self._units or self._units[unit.position] is not unit:
			raise ValueError("Unit is not on the map")

		del self._units[unit.position]

	def move_unit(self, unit, destination):
		"""Move a unit when the destination is valid and reachable."""
		if unit.position not in self._units or self._units[unit.position] is not unit:
			raise ValueError("Unit is not on the map")
		if not self.is_within_bounds(destination):
			raise ValueError("Destination is outside the map")
		if self.is_occupied(destination):
			raise ValueError("Destination is already occupied")

		distance = self._distance(unit.position, destination)
		if distance > unit.movement_range:
			raise ValueError("Destination is outside the unit's movement range")

		del self._units[unit.position]
		unit.set_position(destination)
		self._units[destination] = unit

	@staticmethod
	def _distance(first_position, second_position):
		return sum(
			abs(first_coordinate - second_coordinate)
			for first_coordinate, second_coordinate in zip(
				first_position, second_position
			)
		)

	@staticmethod
	def _is_position(position):
		return (
			isinstance(position, tuple)
			and len(position) == 2
			and all(
				isinstance(coordinate, int) and not isinstance(coordinate, bool)
				for coordinate in position
			)
		)

	@staticmethod
	def _validate_dimension(value, field_name):
		if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
			raise ValueError(f"{field_name} must be a positive integer")