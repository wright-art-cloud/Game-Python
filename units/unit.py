"""Base unit class."""

from abc import ABC, abstractmethod


class Unit(ABC):
	"""Define shared state and behavior for every game unit."""

	def __init__(
		self,
		name,
		health,
		attack_power,
		defense,
		movement_range=1,
		attack_range=1,
		position=(0, 0),
	):
		self._validate_text(name, "Unit name")
		self._validate_positive_integer(health, "Health")
		self._validate_non_negative_integer(attack_power, "Attack power")
		self._validate_non_negative_integer(defense, "Defense")
		self._validate_positive_integer(movement_range, "Movement range")
		self._validate_positive_integer(attack_range, "Attack range")
		self._validate_position(position)

		self._name = name
		self._max_health = health
		self._health = health
		self._attack_power = attack_power
		self._defense = defense
		self._movement_range = movement_range
		self._attack_range = attack_range
		self._position = position

	@property
	def name(self):
		"""Return the unit's name."""
		return self._name

	@property
	def health(self):
		"""Return the unit's current health."""
		return self._health

	@property
	def max_health(self):
		"""Return the unit's starting health."""
		return self._max_health

	@property
	def attack_power(self):
		"""Return the unit's attack power."""
		return self._attack_power

	@property
	def defense(self):
		"""Return the unit's defense value."""
		return self._defense

	@property
	def movement_range(self):
		"""Return the unit's movement range."""
		return self._movement_range

	@property
	def attack_range(self):
		"""Return the unit's attack range."""
		return self._attack_range

	@property
	def position(self):
		"""Return the unit's map position."""
		return self._position

	def set_position(self, position):
		"""Set the unit's position after validating its shape and values."""
		self._validate_position(position)
		self._position = position

	def take_damage(self, amount):
		"""Apply damage after defense and return the damage dealt."""
		self._validate_non_negative_integer(amount, "Damage")
		actual_damage = max(amount - self._defense, 0)
		self._health = max(self._health - actual_damage, 0)
		return actual_damage

	@property
	def is_alive(self):
		"""Return whether the unit still has health."""
		return self._health > 0

	@abstractmethod
	def attack(self, enemy):
		"""Attack an enemy unit using the subclass's rules."""

	@staticmethod
	def _validate_text(value, field_name):
		if not isinstance(value, str) or not value.strip():
			raise ValueError(f"{field_name} cannot be empty")

	@staticmethod
	def _validate_positive_integer(value, field_name):
		if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
			raise ValueError(f"{field_name} must be a positive integer")

	@staticmethod
	def _validate_non_negative_integer(value, field_name):
		if not isinstance(value, int) or isinstance(value, bool) or value < 0:
			raise ValueError(f"{field_name} must be a non-negative integer")

	@staticmethod
	def _validate_position(position):
		if (
			not isinstance(position, tuple)
			or len(position) != 2
			or any(
				not isinstance(coordinate, int) or isinstance(coordinate, bool)
				for coordinate in position
			)
		):
			raise ValueError("Position must be a tuple of two integers")