"""JSON save and load operations."""

import json
from pathlib import Path

from ai.ai_player import AIPlayer
from game.game_engine import Game
from game.map import Map
from game.player import Player
from game.resource import Resource
from units.archer import Archer
from units.soldier import Soldier
from units.tank import Tank


UNIT_TYPES = {
	"Archer": Archer,
	"Soldier": Soldier,
	"Tank": Tank,
}


class SaveManager:
	"""Serialize and restore a Game using JSON files."""

	@staticmethod
	def save_game(game, file_path):
		"""Save the current game state to a JSON file."""
		path = Path(file_path)
		path.parent.mkdir(parents=True, exist_ok=True)
		path.write_text(json.dumps(SaveManager._to_dict(game), indent=2), encoding="utf-8")

	@staticmethod
	def load_game(file_path):
		"""Load a game state from a JSON file."""
		path = Path(file_path)
		with path.open(encoding="utf-8") as save_file:
			data = json.load(save_file)
		return SaveManager._from_dict(data)

	@staticmethod
	def _to_dict(game):
		return {
			"turn_number": game.turn_number,
			"current_player": game.current_player.name,
			"winner": game.winner.name if game.winner else None,
			"map": {
				"width": game.game_map.width,
				"height": game.game_map.height,
			},
			"players": [
				SaveManager._player_to_dict(player)
				for player in game.players
			],
		}

	@staticmethod
	def _player_to_dict(player):
		return {
			"name": player.name,
			"type": "AIPlayer" if isinstance(player, AIPlayer) else "Player",
			"resources": player.resources.as_dict(),
			"units": [SaveManager._unit_to_dict(unit) for unit in player.units],
		}

	@staticmethod
	def _unit_to_dict(unit):
		return {
			"type": type(unit).__name__,
			"name": unit.name,
			"health": unit.health,
			"position": list(unit.position),
		}

	@staticmethod
	def _from_dict(data):
		game_map = Map(data["map"]["width"], data["map"]["height"])
		game = Game(game_map=game_map)
		players_by_name = {}

		for player_data in data["players"]:
			resources = Resource(**player_data["resources"])
			player_class = AIPlayer if player_data["type"] == "AIPlayer" else Player
			player = player_class(player_data["name"], resources=resources)
			game.add_player(player)
			players_by_name[player.name] = player

		for player_data in data["players"]:
			player = players_by_name[player_data["name"]]
			for unit_data in player_data["units"]:
				unit_class = UNIT_TYPES[unit_data["type"]]
				unit = unit_class(
					name=unit_data["name"],
					position=tuple(unit_data["position"]),
				)
				unit._health = unit_data["health"]
				game.add_unit(player, unit)

		game._turn_number = data["turn_number"]
		current_player_name = data["current_player"]
		game._current_player_index = next(
			index
			for index, player in enumerate(game.players)
			if player.name == current_player_name
		)
		winner_name = data["winner"]
		game._winner = players_by_name.get(winner_name)
		return game