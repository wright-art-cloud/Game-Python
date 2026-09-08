"""Game engine and turn management."""

from game.map import Map


class Game:
	"""Coordinate players, the map, turns, combat, and victory state."""

	def __init__(self, game_map=None):
		self._map = game_map or Map()
		self._players = []
		self._current_player_index = 0
		self._turn_number = 1
		self._winner = None

	@property
	def game_map(self):
		"""Return the game's map."""
		return self._map

	@property
	def players(self):
		"""Return registered players without exposing the internal list."""
		return tuple(self._players)

	@property
	def current_player(self):
		"""Return the player whose turn is active."""
		if not self._players:
			return None
		return self._players[self._current_player_index]

	@property
	def turn_number(self):
		"""Return the current turn number."""
		return self._turn_number

	@property
	def winner(self):
		"""Return the winner, or None while the game is undecided."""
		return self._winner

	@property
	def is_over(self):
		"""Return whether a winner has been decided."""
		return self._winner is not None

	def add_player(self, player):
		"""Register a player before the game begins."""
		if self._winner is not None:
			raise ValueError("Cannot add a player after the game is over")
		if player in self._players:
			raise ValueError("Player is already registered")
		if any(existing.name == player.name for existing in self._players):
			raise ValueError("Player names must be unique")

		self._players.append(player)

	def add_unit(self, player, unit):
		"""Give a registered player a unit and place it on the map."""
		self._require_player(player)
		if unit in player.units:
			raise ValueError("Player already owns this unit")

		self._map.add_unit(unit)
		player.add_unit(unit)

	def move_unit(self, player, unit, destination):
		"""Move one of a player's units on the shared map."""
		self._require_active_player(player)
		self._require_owned_unit(player, unit)
		self._map.move_unit(unit, destination)

	def attack(self, player, attacker, target):
		"""Resolve an attack and remove a defeated unit from the game."""
		self._require_active_player(player)
		self._require_owned_unit(player, attacker)
		target_owner = self._owner_of(target)
		if target_owner is None or target_owner is player:
			raise ValueError("Target must belong to another registered player")
		if not target.is_alive:
			raise ValueError("Target is already defeated")
		if self._distance(attacker.position, target.position) > attacker.attack_range:
			raise ValueError("Target is outside the attack range")

		damage = attacker.attack(target)
		if not target.is_alive:
			target_owner.remove_unit(target)
			self._map.remove_unit(target)
			if not target_owner.units:
				self._winner = player

		return damage

	def end_turn(self):
		"""Move control to the next registered player."""
		if len(self._players) < 2:
			raise ValueError("At least two players are required to end a turn")
		if self.is_over:
			raise ValueError("Cannot end the turn after the game is over")

		self._current_player_index = (
			self._current_player_index + 1
		) % len(self._players)
		if self._current_player_index == 0:
			self._turn_number += 1

	def _require_player(self, player):
		if player not in self._players:
			raise ValueError("Player is not registered")

	def _require_active_player(self, player):
		self._require_player(player)
		if self.current_player is not player:
			raise ValueError("It is not this player's turn")
		if self.is_over:
			raise ValueError("The game is over")

	def _require_owned_unit(self, player, unit):
		if unit not in player.units:
			raise ValueError("Unit does not belong to this player")

	def _owner_of(self, unit):
		for player in self._players:
			if unit in player.units:
				return player
		return None

	@staticmethod
	def _distance(first_position, second_position):
		return sum(
			abs(first_coordinate - second_coordinate)
			for first_coordinate, second_coordinate in zip(
				first_position, second_position
			)
		)