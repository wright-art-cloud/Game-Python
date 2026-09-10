"""Tests for resource management."""

import pytest

from game.resource import Resource


def test_resource_stores_initial_amounts():
	resources = Resource(gold=100, food=50, wood=25)

	assert resources.as_dict() == {
		"gold": 100,
		"food": 50,
		"wood": 25,
	}


def test_resource_can_add_and_spend():
	resources = Resource(gold=100)

	resources.add("gold", 25)
	resources.spend("gold", 40)

	assert resources.get("gold") == 85


def test_as_dict_returns_a_copy():
	resources = Resource(gold=100)
	displayed_resources = resources.as_dict()
	displayed_resources["gold"] = 0

	assert resources.get("gold") == 100


def test_unknown_resource_type_is_rejected():
	resources = Resource()

	with pytest.raises(ValueError, match="Unknown resource type"):
		resources.get("stone")


def test_negative_amount_is_rejected():
	with pytest.raises(ValueError, match="cannot be negative"):
		Resource(gold=-1)


def test_non_integer_amount_is_rejected():
	with pytest.raises(TypeError, match="must be integers"):
		Resource(gold=2.5)


def test_spending_more_than_available_is_rejected():
	resources = Resource(gold=10)

	with pytest.raises(ValueError, match="Insufficient resources"):
		resources.spend("gold", 11)