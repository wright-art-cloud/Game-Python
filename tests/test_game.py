"""Tests for the game engine."""

import game
import pytest

from game.engine import Game
from game.map import Map
from game.player import Player
from units.archer import Archer
from units.soldier import Soldier


def test_project_packages_import():
    """The planned package structure can be imported by Python."""
    import ai
    import game
    import units

    assert ai is not None
    assert game is not None
    assert units is not None


def test_game_registers_players_and_tracks_turns():
    game = Game()
    first_player = Player("Player 1")
    second_player = Player("Player 2")

    game.add_player(first_player)
    game.add_player(second_player)

    assert game.players == (first_player, second_player)
    assert game.current_player is first_player
    assert game.turn_number == 1

    game.end_turn()

    assert game.current_player is second_player
    assert game.turn_number == 1

    game.end_turn()

    assert game.current_player is first_player
    assert game.turn_number == 2


def test_game_adds_and_moves_a_player_unit():
    game = Game(game_map=Map(width=5, height=5))
    player = Player("Player 1")
    game.add_player(player)
    game.add_player(Player("Player 2"))
    unit = Soldier(position=(1, 1))
    game.add_unit(player, unit)

    game.move_unit(player, unit, (2, 2))

    assert unit in player.units
    assert game.game_map.get_unit_at((2, 2)) is unit


def test_game_resolves_polymorphic_attack_and_victory():
    game = Game(game_map=Map(width=5, height=5))
    first_player = Player("Player 1")
    second_player = Player("Player 2")
    game.add_player(first_player)
    game.add_player(second_player)
    attacker = Archer(position=(1, 1))
    target = Soldier(position=(1, 3))
    game.add_unit(first_player, attacker)
    game.add_unit(second_player, target)

    damage = game.attack(first_player, attacker, target)

    assert damage == 13
    assert target.health == 87
    assert game.is_over is False

    game.game_map.move_unit(target, (1, 2))
    while target.is_alive:
        game.attack(first_player, attacker, target)

    assert game.winner is first_player
    assert game.is_over is True
    assert target not in second_player.units
    assert game.game_map.get_unit_at((1, 2)) is None


def test_game_rejects_actions_during_another_players_turn():
    game = Game()
    first_player = Player("Player 1")
    second_player = Player("Player 2")
    game.add_player(first_player)
    game.add_player(second_player)
    unit = Soldier(position=(0, 0))
    game.add_unit(first_player, unit)

    game.end_turn()

    with pytest.raises(ValueError, match="not this player's turn"):
        game.move_unit(first_player, unit, (1, 0))


def test_game_rejects_duplicate_player_names():
    game = Game()
    game.add_player(Player("Player 1"))

    with pytest.raises(ValueError, match="unique"):
        game.add_player(Player("Player 1"))