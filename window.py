"""Pygame window for the turn-based strategy game."""

import pygame

from game.resource import ResourceNode
from main import create_game


BOARD_SIZE = 64
PANEL_WIDTH = 260
MARGIN = 24
WINDOW_WIDTH = MARGIN * 2 + BOARD_SIZE * 8 + PANEL_WIDTH
WINDOW_HEIGHT = MARGIN * 2 + BOARD_SIZE * 8

BACKGROUND = (24, 29, 36)
PANEL = (34, 41, 51)
GRID_LIGHT = (211, 215, 204)
GRID_DARK = (167, 178, 164)
TEXT = (239, 241, 235)
MUTED_TEXT = (173, 183, 177)
PLAYER_COLORS = ((49, 104, 190), (190, 67, 61))
RESOURCE_COLORS = {
    "gold": (225, 179, 55),
    "food": (83, 161, 91),
    "wood": (151, 99, 53),
}


def create_window_game():
    """Create the standard game and place collectible resources on its map."""
    game = create_game()
    resources = (
        ResourceNode((3, 2), "gold", 20),
        ResourceNode((4, 4), "food", 20),
        ResourceNode((2, 5), "wood", 20),
        ResourceNode((5, 3), "gold", 20),
    )
    for resource in resources:
        game.game_map.add_resource(resource)
    return game


def run(game=None):
    """Run the graphical game until the window is closed."""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Grid Strategy Game")
    clock = pygame.time.Clock()
    fonts = {
        "title": pygame.font.SysFont("dejavusans", 24, bold=True),
        "body": pygame.font.SysFont("dejavusans", 18),
        "small": pygame.font.SysFont("dejavusans", 15),
    }
    game = game or create_window_game()
    selected_index = 0
    status = "Use the arrow keys to move."
    running = True

    while running:
        active_units = game.current_player.units
        if active_units:
            selected_index %= len(active_units)
            selected_unit = active_units[selected_index]
        else:
            selected_unit = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_TAB and active_units:
                    selected_index = (selected_index + 1) % len(active_units)
                    status = f"Selected {active_units[selected_index].name}."
                elif event.key in (pygame.K_RETURN, pygame.K_e):
                    try:
                        game.end_turn()
                        selected_index = 0
                        status = f"{game.current_player.name}'s turn."
                    except ValueError as error:
                        status = str(error)
                elif event.key in (
                    pygame.K_UP,
                    pygame.K_DOWN,
                    pygame.K_LEFT,
                    pygame.K_RIGHT,
                ):
                    if selected_unit is None:
                        status = "This player has no units."
                    else:
                        offsets = {
                            pygame.K_UP: (0, -1),
                            pygame.K_DOWN: (0, 1),
                            pygame.K_LEFT: (-1, 0),
                            pygame.K_RIGHT: (1, 0),
                        }
                        try:
                            status = move_selected(game, selected_unit, offsets[event.key])
                        except ValueError as error:
                            status = str(error)

        draw_game(screen, game, selected_unit, status, fonts)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def move_selected(game, unit, offset):
    """Move a selected unit one tile and describe any collected resource."""
    x_coordinate, y_coordinate = unit.position
    delta_x, delta_y = offset
    destination = (x_coordinate + delta_x, y_coordinate + delta_y)
    resource = game.move_unit(game.current_player, unit, destination)
    if resource is None:
        return f"{unit.name} moved to {destination}."
    return (
        f"Collected {resource.amount} {resource.resource_type} "
        f"at {destination}."
    )


def draw_game(screen, game, selected_unit, status, fonts):
    """Draw the board, units, resources, and current player panel."""
    screen.fill(BACKGROUND)
    draw_board(screen, game, selected_unit, fonts["body"])

    panel_x = MARGIN + BOARD_SIZE * game.game_map.width + MARGIN
    pygame.draw.rect(
        screen,
        PANEL,
        (panel_x, MARGIN, PANEL_WIDTH, BOARD_SIZE * game.game_map.height),
        border_radius=8,
    )
    draw_text(screen, fonts["title"], "Strategy Game", panel_x + 18, MARGIN + 18)
    draw_text(
        screen,
        fonts["body"],
        f"Turn {game.turn_number}: {game.current_player.name}",
        panel_x + 18,
        MARGIN + 58,
    )

    y_position = MARGIN + 105
    for index, player in enumerate(game.players):
        draw_text(screen, fonts["body"], player.name, panel_x + 18, y_position,
                  PLAYER_COLORS[index])
        y_position += 28
        resources = player.resources.as_dict()
        draw_text(
            screen,
            fonts["small"],
            f"Gold {resources['gold']}  Food {resources['food']}",
            panel_x + 18,
            y_position,
            MUTED_TEXT,
        )
        y_position += 22
        draw_text(
            screen,
            fonts["small"],
            f"Wood {resources['wood']}",
            panel_x + 18,
            y_position,
            MUTED_TEXT,
        )
        y_position += 38

    draw_text(screen, fonts["small"], "Controls", panel_x + 18, y_position)
    y_position += 25
    for control in ("Arrows  Move unit", "Tab  Select unit", "E / Enter  End turn", "Esc  Quit"):
        draw_text(screen, fonts["small"], control, panel_x + 18, y_position, MUTED_TEXT)
        y_position += 21

    draw_text(screen, fonts["small"], status, panel_x + 18, WINDOW_HEIGHT - 60, TEXT)


def draw_board(screen, game, selected_unit, font):
    """Draw map cells and their contents."""
    for y_coordinate in range(game.game_map.height):
        for x_coordinate in range(game.game_map.width):
            cell = pygame.Rect(
                MARGIN + x_coordinate * BOARD_SIZE,
                MARGIN + y_coordinate * BOARD_SIZE,
                BOARD_SIZE,
                BOARD_SIZE,
            )
            color = GRID_LIGHT if (x_coordinate + y_coordinate) % 2 == 0 else GRID_DARK
            pygame.draw.rect(screen, color, cell)
            position = (x_coordinate, y_coordinate)
            resource = game.game_map.get_resource_at(position)
            if resource is not None:
                pygame.draw.circle(screen, RESOURCE_COLORS[resource.resource_type], cell.center, 17)
                draw_centered_text(screen, font, resource.resource_type[0].upper(), cell.center)

            unit = game.game_map.get_unit_at(position)
            if unit is not None:
                player_index = next(
                    index for index, player in enumerate(game.players) if unit in player.units
                )
                unit_color = PLAYER_COLORS[player_index]
                pygame.draw.circle(screen, unit_color, cell.center, 23)
                draw_centered_text(screen, font, unit.name[0].upper(), cell.center)
                if unit is selected_unit:
                    pygame.draw.circle(screen, (255, 244, 181), cell.center, 28, 3)


def draw_text(screen, font, text, x_position, y_position, color=TEXT):
    """Draw left-aligned text."""
    screen.blit(font.render(text, True, color), (x_position, y_position))


def draw_centered_text(screen, font, text, center):
    """Draw text centered at a point."""
    surface = font.render(text, True, TEXT)
    screen.blit(surface, surface.get_rect(center=center))


if __name__ == "__main__":
    run()
