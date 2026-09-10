"""Soldier unit type."""

from units.unit import Unit


class Soldier(Unit):
	"""Balanced short-range unit."""

	def __init__(self, name="Soldier", position=(0, 0)):
		super().__init__(
			name=name,
			health=100,
			attack_power=20,
			defense=5,
			movement_range=2,
			attack_range=1,
			position=position,
		)

	def attack(self, enemy):
		"""Deal the soldier's standard attack damage."""
		return enemy.take_damage(self.attack_power)