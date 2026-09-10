"""Entry point and terminal interface for the strategy game."""

from game.game_engine import Game
from game.map import Map
from game.player import Player
from units.archer import Archer
from units.soldier import Soldier
from units.tank import Tank


UNIT_TYPES = {
    "1": ("Soldier", Soldier, {"gold": 30, "food": 20, "wood": 10}),
    "2": ("Archer", Archer, {"gold": 40, "food": 15, "wood": 20}),
    "3": ("Tank", Tank, {"gold": 80, "food": 40, "wood": 30}),
}


def main():
    """Create a game and run the terminal interface."""
    game = create_game()
    print("Terminal Strategy Game")
    print("Defeat the other player's units to win.")

    while not game.is_over:
        display_status(game)
        display_menu()
        choice = input("Choose an action: ").strip()

        if choice == "0":
            print("Goodbye!")
            return

        try:
            handle_action(game, choice)
        except ValueError as error:
            print(f"Action could not be completed: {error}")

    print(f"{game.winner.name} wins the game!")


def create_game():
    """Create the initial two-player game state."""
    game = Game(game_map=Map(width=8, height=8))
    first_player = Player("Player 1")
    second_player = Player("Player 2")
    first_player.collect_resource("gold", 100)
    first_player.collect_resource("food", 100)
    first_player.collect_resource("wood", 100)
    second_player.collect_resource("gold", 100)
    second_player.collect_resource("food", 100)
    second_player.collect_resource("wood", 100)
    game.add_player(first_player)
    game.add_player(second_player)
    game.add_unit(first_player, Soldier("P1 Soldier", position=(1, 1)))
    game.add_unit(second_player, Soldier("P2 Soldier", position=(6, 6)))
    return game


def display_menu():
    """Print the actions available during a turn."""
    print("\n1. View map")
    print("2. View units")
    print("3. Move unit")
    print("4. Attack")
    print("5. Gather resources")
    print("6. Build unit")
    print("7. View resources")
    print("8. End turn")
    print("0. Quit")


def display_status(game):
    """Display the current turn and active player."""
    print(
        f"\nTurn {game.turn_number} | "
        f"Active player: {game.current_player.name}"
    )


def handle_action(game, choice):
    """Execute one selected menu action."""
    actions = {
        "1": display_map,
        "2": display_units,
        "3": move_unit,
        "4": attack_unit,
        "5": gather_resources,
        "6": build_unit,
        "7": display_resources,
        "8": end_turn,
    }
    action = actions.get(choice)
    if action is None:
        print("Please choose a number from the menu.")
        return
    action(game)


def display_map(game):
    """Print the map using unit initials and dots for empty cells."""
    game_map = game.game_map
    print("\nMap:")
    for y_coordinate in range(game_map.height):
        row = []
        for x_coordinate in range(game_map.width):
            unit = game_map.get_unit_at((x_coordinate, y_coordinate))
            row.append(unit.name[0].upper() if unit else ".")
        print(" ".join(row))


def display_units(game):
    """Print every player's unit position and health."""
    for player in game.players:
        print(f"\n{player.name} units:")
        for unit in player.units:
            print(
                f"- {unit.name}: position={unit.position}, "
                f"health={unit.health}/{unit.max_health}"
            )


def display_resources(game):
    """Print the active player's resources."""
    print(game.current_player.resources.as_dict())


def move_unit(game):
    """Read a unit and destination, then move it."""
    player = game.current_player
    unit = choose_owned_unit(player)
    destination = read_position("Enter destination as x y: ")
    game.move_unit(player, unit, destination)
    print(f"{unit.name} moved to {destination}.")


def attack_unit(game):
    """Read an attacker and target, then resolve combat."""
    player = game.current_player
    attacker = choose_owned_unit(player)
    target_player = choose_opponent(game, player)
    target = choose_owned_unit(target_player)
    damage = game.attack(player, attacker, target)
    print(f"{attacker.name} dealt {damage} damage to {target.name}.")


def gather_resources(game):
    """Give the active player one unit of each resource type."""
    player = game.current_player
    for resource_type in ("gold", "food", "wood"):
        player.collect_resource(resource_type, 10)
    print("Collected 10 gold, 10 food, and 10 wood.")


def build_unit(game):
    """Build a selected unit when the active player can pay its cost."""
    player = game.current_player
    print("1. Soldier (30 gold, 20 food, 10 wood)")
    print("2. Archer (40 gold, 15 food, 20 wood)")
    print("3. Tank (80 gold, 40 food, 30 wood)")
    unit_choice = input("Choose a unit: ").strip()
    unit_data = UNIT_TYPES.get(unit_choice)
    if unit_data is None:
        raise ValueError("Unknown unit type")

    unit_name, unit_class, cost = unit_data
    for resource_type, amount in cost.items():
        if player.resources.get(resource_type) < amount:
            raise ValueError(f"Not enough {resource_type} to build {unit_name}")

    position = find_empty_position(game, player)
    for resource_type, amount in cost.items():
        player.spend_resource(resource_type, amount)
    unit_number = len(player.units) + 1
    unit = unit_class(f"{unit_name} {player.name} {unit_number}", position=position)
    game.add_unit(player, unit)
    print(f"Built {unit.name} at {position}.")


def end_turn(game):
    """End the active player's turn."""
    game.end_turn()
    print(f"It is now {game.current_player.name}'s turn.")


def choose_owned_unit(player):
    """Choose one unit from a player's army by number."""
    if not player.units:
        raise ValueError(f"{player.name} has no units")
    for index, unit in enumerate(player.units, start=1):
        print(f"{index}. {unit.name} at {unit.position}")
    unit_number = read_integer("Choose a unit: ")
    if not 1 <= unit_number <= len(player.units):
        raise ValueError("Invalid unit number")
    return player.units[unit_number - 1]


def choose_opponent(game, player):
    """Return the other registered player."""
    opponents = [opponent for opponent in game.players if opponent is not player]
    if not opponents:
        raise ValueError("No opponent is available")
    return opponents[0]


def find_empty_position(game, player):
    """Find a free cell near the player's existing units."""
    preferred_x = 1 if player is game.players[0] else game.game_map.width - 2
    preferred_y = 1 if player is game.players[0] else game.game_map.height - 2
    for radius in range(max(game.game_map.width, game.game_map.height)):
        for x_coordinate in range(game.game_map.width):
            for y_coordinate in range(game.game_map.height):
                position = (x_coordinate, y_coordinate)
                if (
                    abs(x_coordinate - preferred_x) + abs(y_coordinate - preferred_y)
                    == radius
                    and not game.game_map.is_occupied(position)
                ):
                    return position
    raise ValueError("The map is full")


def read_integer(prompt):
    """Read an integer from terminal input."""
    try:
        return int(input(prompt).strip())
    except ValueError as error:
        raise ValueError("Please enter a whole number") from error


def read_position(prompt):
    """Read an x/y coordinate from terminal input."""
    values = input(prompt).split()
    if len(values) != 2:
        raise ValueError("Enter exactly two coordinates")
    try:
        return tuple(int(value) for value in values)
    except ValueError as error:
        raise ValueError("Coordinates must be whole numbers") from error
if __name__ == "__main__":
    main()