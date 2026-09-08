"""Tests for unit types and combat."""

import pytest

from units.unit import Unit
from units.archer import Archer
from units.soldier import Soldier
from units.tank import Tank


class TrainingUnit(Unit):
	"""Small concrete unit used to test the abstract base class."""

	def attack(self, enemy):
		return enemy.take_damage(self.attack_power)


def test_unit_stores_common_attributes():
	unit = TrainingUnit(
		"Training Soldier",
		health=100,
		attack_power=25,
		defense=5,
		movement_range=2,
		attack_range=1,
		position=(3, 4),
	)

	assert unit.name == "Training Soldier"
	assert unit.health == 100
	assert unit.max_health == 100
	assert unit.attack_power == 25
	assert unit.defense == 5
	assert unit.movement_range == 2
	assert unit.attack_range == 1
	assert unit.position == (3, 4)
	assert unit.is_alive is True


def test_unit_takes_damage_after_defense():
	unit = TrainingUnit("Target", health=100, attack_power=10, defense=5)

	actual_damage = unit.take_damage(20)

	assert actual_damage == 15
	assert unit.health == 85


def test_unit_health_cannot_become_negative():
	unit = TrainingUnit("Target", health=20, attack_power=10, defense=0)

	unit.take_damage(100)

	assert unit.health == 0
	assert unit.is_alive is False


def test_subclass_attack_uses_polymorphism():
	attacker = TrainingUnit("Attacker", health=100, attack_power=20, defense=0)
	target = TrainingUnit("Target", health=100, attack_power=10, defense=5)

	attacker.attack(target)

	assert target.health == 85


def test_position_can_be_changed():
	unit = TrainingUnit("Scout", health=50, attack_power=5, defense=1)

	unit.set_position((2, 7))

	assert unit.position == (2, 7)


def test_unit_requires_a_concrete_attack_implementation():
	with pytest.raises(TypeError):
		Unit("Abstract", health=10, attack_power=1, defense=0)


@pytest.mark.parametrize(
	"kwargs",
	[
		{"health": 0},
		{"attack_power": -1},
		{"defense": -1},
		{"movement_range": 0},
		{"attack_range": 0},
	]
)
def test_invalid_unit_stats_are_rejected(kwargs):
	valid_stats = {
		"health": 100,
		"attack_power": 10,
		"defense": 5,
		"movement_range": 1,
		"attack_range": 1,
	}
	valid_stats.update(kwargs)

	with pytest.raises(ValueError):
		TrainingUnit("Invalid", **valid_stats)


@pytest.mark.parametrize(
	"unit_class, expected_stats",
	[
		(Soldier, {"health": 100, "attack_power": 20, "defense": 5,
			"movement_range": 2, "attack_range": 1}),
		(Archer, {"health": 75, "attack_power": 18, "defense": 2,
			"movement_range": 2, "attack_range": 3}),
		(Tank, {"health": 160, "attack_power": 30, "defense": 10,
			"movement_range": 1, "attack_range": 1}),
	],
)
def test_concrete_units_have_distinct_roles(unit_class, expected_stats):
	unit = unit_class(position=(2, 3))

	for attribute, expected_value in expected_stats.items():
		assert getattr(unit, attribute) == expected_value
	assert unit.position == (2, 3)


@pytest.mark.parametrize("unit_class", [Soldier, Archer, Tank])
def test_concrete_units_override_attack(unit_class):
	attacker = unit_class()
	target = TrainingUnit("Target", health=100, attack_power=1, defense=0)

	actual_damage = attacker.attack(target)

	assert actual_damage == attacker.attack_power
	assert target.health == 100 - attacker.attack_power