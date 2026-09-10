"""Tests for JSON save and load operations."""

from ai.ai_player import AIPlayer
from game.game import Game
from game.map import Map
from game.player import Player
from game.resource import Resource
from game.save_manager import SaveManager
from units.archer import Archer
from units.soldier import Soldier


def test_save_and_load_preserves_game_state(tmp_path):
	game = Game(Map(width=7, height=6))
	first_player = Player("Player 1", Resource(gold=80, food=60, wood=40))
	second_player = AIPlayer("Computer", Resource(gold=50, food=30, wood=20))
	game.add_player(first_player)
	game.add_player(second_player)
	game.add_unit(first_player, Archer("Longbow", position=(1, 2)))
	game.add_unit(second_player, Soldier("Guard", position=(5, 4)))
	game.game_map.move_unit(first_player.units[0], (2, 2))
	first_player.units[0].take_damage(10)
	game.end_turn()

	save_path = tmp_path / "campaign.json"
	SaveManager.save_game(game, save_path)
	loaded_game = SaveManager.load_game(save_path)

	assert loaded_game.game_map.width == 7
	assert loaded_game.game_map.height == 6
	assert loaded_game.turn_number == 1
	assert loaded_game.current_player.name == "Computer"
	assert loaded_game.current_player is loaded_game.players[1]
	assert isinstance(loaded_game.players[1], AIPlayer)
	assert loaded_game.players[0].resources.as_dict() == {
		"gold": 80,
		"food": 60,
		"wood": 40,
	}
	loaded_unit = loaded_game.players[0].units[0]
	assert isinstance(loaded_unit, Archer)
	assert loaded_unit.position == (2, 2)
	assert loaded_unit.health == 67