"""Archer unit type."""

from units.unit import Unit


class Archer(Unit):
	"""Long-range unit with lower defense."""

	def __init__(self, name="Archer", position=(0, 0)):
		super().__init__(
			name=name,
			health=75,
			attack_power=18,
			defense=2,
			movement_range=2,
			attack_range=3,
			position=position,
		)

	def attack(self, enemy):
		"""Deal the archer's ranged attack damage."""
		return enemy.take_damage(self.attack_power)