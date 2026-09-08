"""Tests for the rule-based AI player."""

from ai.ai_player import AIPlayer
from game.game import Game
from game.map import Map
from game.player import Player
from units.soldier import Soldier


def test_ai_attacks_when_enemy_is_in_range():
	game = Game(Map(width=5, height=5))
	ai_player = AIPlayer("Computer")
	human_player = Player("Human")
	game.add_player(ai_player)
	game.add_player(human_player)
	attacker = Soldier(position=(1, 1))
	target = Soldier(position=(1, 2))
	game.add_unit(ai_player, attacker)
	game.add_unit(human_player, target)

	result = ai_player.take_turn(game)

	assert result == "attack"
	assert target.health == 85


def test_ai_moves_toward_enemy_when_attack_is_not_possible():
	game = Game(Map(width=8, height=8))
	ai_player = AIPlayer("Computer")
	human_player = Player("Human")
	game.add_player(ai_player)
	game.add_player(human_player)
	unit = Soldier(position=(1, 1))
	target = Soldier(position=(6, 6))
	game.add_unit(ai_player, unit)
	game.add_unit(human_player, target)

	result = ai_player.take_turn(game)

	assert result == "move"
	assert unit.position == (2, 1)