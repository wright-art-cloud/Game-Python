"""Tests for the player component."""

import pytest

from game.player import Player
from game.resource import Resource


def test_player_starts_with_name_and_empty_state():
	player = Player("Commander")

	assert player.name == "Commander"
	assert player.units == ()
	assert player.resources.as_dict() == {
		"gold": 0,
		"food": 0,
		"wood": 0,
	}


def test_player_can_use_existing_resources():
	resources = Resource(gold=50)
	player = Player("Commander", resources=resources)

	player.collect_resource("gold", 25)
	player.spend_resource("gold", 10)

	assert player.resources is resources
	assert player.resources.get("gold") == 65


def test_player_can_add_and_remove_units():
	player = Player("Commander")
	first_unit = object()
	second_unit = object()

	player.add_unit(first_unit)
	player.add_unit(second_unit)
	player.remove_unit(first_unit)

	assert player.units == (second_unit,)


def test_units_property_does_not_expose_internal_list():
	player = Player("Commander")
	unit = object()
	player.add_unit(unit)
	visible_units = player.units

	assert isinstance(visible_units, tuple)
	assert visible_units == (unit,)


def test_empty_player_name_is_rejected():
	with pytest.raises(ValueError, match="cannot be empty"):
		Player(" ")