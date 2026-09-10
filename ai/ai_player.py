"""AI-controlled player behavior."""

from ai.player_ai import AIPlayer


class AIPlayer(AIPlayer):
	"""Player that makes simple rule-based decisions."""

	def take_turn(self, game):
		"""Attack a reachable enemy or move one unit toward an enemy."""
		if game.current_player is not self:
			raise ValueError("It is not this player's turn")

		enemy = self._find_enemy(game)
		if enemy is None or not self.units:
			return "no_action"

		for unit in self.units:
			target = self._target_in_range(unit, enemy)
			if target is not None:
				game.attack(self, unit, target)
				return "attack"

		unit = self.units[0]
		destination = self._step_toward(unit.position, enemy.units[0].position)
		if (
			game.game_map.is_within_bounds(destination)
			and not game.game_map.is_occupied(destination)
		):
			game.move_unit(self, unit, destination)
			return "move"

		return "no_action"

	def _find_enemy(self, game):
		for player in game.players:
			if player is not self and player.units:
				return player
		return None

	@staticmethod
	def _target_in_range(unit, enemy):
		for target in enemy.units:
			distance = sum(
				abs(first - second)
				for first, second in zip(unit.position, target.position)
			)
			if distance <= unit.attack_range:
				return target
		return None

	@staticmethod
	def _step_toward(start, destination):
		x_coordinate, y_coordinate = start
		target_x, target_y = destination
		if x_coordinate != target_x:
			x_coordinate += 1 if target_x > x_coordinate else -1
		elif y_coordinate != target_y:
			y_coordinate += 1 if target_y > y_coordinate else -1
		return x_coordinate, y_coordinate