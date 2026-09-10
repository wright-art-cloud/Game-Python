"""Tank unit type."""

from units.unit import Unit


class Tank(Unit):
	"""Slow, heavily defended unit."""

	def __init__(self, name="Tank", position=(0, 0)):
		super().__init__(
			name=name,
			health=160,
			attack_power=30,
			defense=10,
			movement_range=1,
			attack_range=1,
			position=position,
		)

	def attack(self, enemy):
		"""Deal the tank's powerful attack damage."""
		return enemy.take_damage(self.attack_power)