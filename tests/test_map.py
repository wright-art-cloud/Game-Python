"""Tests for the map component."""

import pytest

from game.map import Map
from units.base_unit import Unit


def test_map_stores_dimensions():
	game_map = Map(width=8, height=6)

	assert game_map.width == 8
	assert game_map.height == 6
	assert game_map.units == ()


def test_map_identifies_valid_coordinates():
	game_map = Map(width=5, height=4)

	assert game_map.is_within_bounds((0, 0)) is True
	assert game_map.is_within_bounds((4, 3)) is True
	assert game_map.is_within_bounds((5, 3)) is False
	assert game_map.is_within_bounds((-1, 0)) is False
	assert game_map.is_within_bounds([1, 1]) is False


def test_map_adds_and_finds_a_unit():
	game_map = Map(width=5, height=5)
	unit = Soldier(position=(2, 3))

	game_map.add_unit(unit)

	assert game_map.get_unit_at((2, 3)) is unit
	assert game_map.is_occupied((2, 3)) is True
	assert game_map.units == (unit,)


def test_map_moves_unit_within_movement_range():
	game_map = Map(width=5, height=5)
	unit = Soldier(position=(1, 1))
	game_map.add_unit(unit)

	game_map.move_unit(unit, (2, 2))

	assert unit.position == (2, 2)
	assert game_map.get_unit_at((1, 1)) is None
	assert game_map.get_unit_at((2, 2)) is unit


def test_map_rejects_out_of_range_movement():
	game_map = Map(width=10, height=10)
	unit = Soldier(position=(1, 1))
	game_map.add_unit(unit)

	with pytest.raises(ValueError, match="movement range"):
		game_map.move_unit(unit, (4, 1))


def test_map_rejects_invalid_and_occupied_destinations():
	game_map = Map(width=5, height=5)
	first_unit = Soldier(position=(1, 1))
	second_unit = Soldier(position=(2, 1))
	game_map.add_unit(first_unit)
	game_map.add_unit(second_unit)

	with pytest.raises(ValueError, match="occupied"):
		game_map.move_unit(first_unit, (2, 1))
	with pytest.raises(ValueError, match="outside the map"):
		game_map.move_unit(first_unit, (-1, 1))


def test_map_rejects_duplicate_placements():
	game_map = Map(width=5, height=5)
	first_unit = Soldier(position=(1, 1))
	second_unit = Soldier(position=(1, 1))
	game_map.add_unit(first_unit)

	with pytest.raises(ValueError, match="occupied"):
		game_map.add_unit(second_unit)


def test_map_removes_a_unit():
	game_map = Map(width=5, height=5)
	unit = Soldier(position=(1, 1))
	game_map.add_unit(unit)

	game_map.remove_unit(unit)

	assert game_map.units == ()
	assert game_map.is_occupied((1, 1)) is False