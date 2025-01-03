import pygame
from typing import Tuple


BLACK = (7, 6, 0)
RED = (234, 82, 111)
WHITE = (247,247, 255)
BLUE = (39, 154, 241)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 128, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
LIME = (0, 255, 0)
PINK = (255, 192, 203)
BROWN = (165, 42, 42)
GREY = (128, 128, 128)
NAVY = (0, 0, 128)
TEAL = (0, 128, 128)
MAROON = (128, 0, 0)
OLIVE = (128, 128, 0)
CORAL = (255, 127, 80)
SALMON = (250, 128, 114)
VIOLET = (238, 130, 238)
INDIGO = (75, 0, 130)
GOLD = (255, 215, 0)
TURQUOISE = (64, 224, 208)
LIGHT_GREEN = (173, 255, 47)
DARK_GREEN = (34, 139, 34)

colors = {
    0: BLUE,
    1: RED,
    2: WHITE,
    3: BLACK,
    4: ORANGE,
    5: YELLOW,
    6: GREEN,
    7: PURPLE,
    8: CYAN,
    9: MAGENTA,
    10: LIME,
    11: PINK,
    12: BROWN,
    13: GREY,
    14: NAVY,
    15: TEAL,
    16: MAROON,
    17: OLIVE,
    18: CORAL,
    19: SALMON,
    20: VIOLET,
    21: INDIGO,
    22: GOLD,
    23: TURQUOISE
}


def draw_bullet(surface, position, angle, size=(10, 50)):
    """
    :param surface: Surface on which the bullet is drawn
    :param position: Tuple (x, y) for the central position of the bale
    :param angle: Rotation angle in degrees
    :param size: Size of the bale as a tuple (width, height)
    """
    width, height = size
    bullet_surface = pygame.Surface((width, height), pygame.SRCALPHA)  # Crear superficie transparente

    pygame.draw.rect(bullet_surface, YELLOW, (0, 10, width, height - 20))

    pygame.draw.polygon(bullet_surface, YELLOW, [
        (width // 2, 0),
        (0, 10),
        (width, 10)
    ])

    pygame.draw.rect(bullet_surface, BLACK, (2, 10, width - 4, 5))

    rotated_bullet = pygame.transform.rotate(bullet_surface, -angle)
    rect = rotated_bullet.get_rect(center=position)

    surface.blit(rotated_bullet, rect.center)


def darken_color(color: Tuple[int, int, int], factor: float = 0.2) -> Tuple[int, int, int]:
    """Returns a darker color based on the original color."""
    return (
        max(0, int(color[0] * (1 - factor))),
        max(0, int(color[1] * (1 - factor))),
        max(0, int(color[2] * (1 - factor)))
    )


def create_tank_surface(color: Tuple[int, int, int]) -> pygame.Surface:
    """ Create a new tank surface """
    dark_gray = (64, 64, 64)
    light_gray = (128, 128, 128)
    tank_surface = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
    pygame.draw.rect(tank_surface, color, (10, 4, 12, 24), border_radius=2)  # Draw rect green

    # Draw gray rect on the sides, adjusted to connect with the green part
    pygame.draw.rect(tank_surface, dark_gray, (4, 4, 6, 24), border_radius=2)  # Left
    pygame.draw.rect(tank_surface, dark_gray, (22, 4, 6, 24), border_radius=2)  # Right

    # Adjust the position of the wheels to connect with the green part
    for i in range(4, 24, 4):
        pygame.draw.rect(tank_surface, light_gray, (4, i + 2, 6, 2), border_radius=1)  # Left
        pygame.draw.rect(tank_surface, light_gray, (22, i + 2, 6, 2), border_radius=1)  # Right

    return tank_surface


def create_cannon_surface(color: Tuple[int, int, int]) -> pygame.Surface:
    DARK_LOCAL = darken_color(color)
    LIGHT_LOCAL = darken_color(color, factor=0.1)
    cannon_surface = pygame.Surface((10, 26), pygame.SRCALPHA)

    # Adjust the drawing to fit the new size (10x26)
    pygame.draw.rect(cannon_surface, DARK_LOCAL, (0, 14, 10, 12), border_radius=2)  # Main body
    pygame.draw.rect(cannon_surface, LIGHT_LOCAL, (2, 0, 6, 14), border_radius=0)  # Top part
    pygame.draw.rect(cannon_surface, YELLOW, (3, 8, 4, 6), border_radius=0)  # Center detail
    pygame.draw.rect(cannon_surface, LIGHT_GREEN, (3, -2, 4, 10), border_radius=0)  # Top detail

    return cannon_surface


def tank_cover(color, pos, screen: pygame.Surface, scale=(32,32), angle=200, angle_cannon= 0):
    tank_surface = pygame.Surface(scale, pygame.SRCALPHA)
    tank_body = pygame.transform.scale(create_tank_surface(colors[color]), scale)

    scale_cannon = (10* scale[0]//32, 26* scale[1]//32)
    tank_cannon = pygame.transform.scale(create_cannon_surface(colors[color]),scale_cannon)

    angle = angle % 360
    angle_cannon = angle_cannon % 360

    rotated_body = pygame.transform.rotate(tank_body, angle)
    rotated_cannon = pygame.transform.rotate(tank_cannon, angle_cannon)

    cannon_rect = rotated_cannon.get_rect(center=(tank_surface.get_width() // 2, tank_surface.get_height() // 2))
    body_rect = rotated_body.get_rect(center=(tank_surface.get_width() // 2, tank_surface.get_height() // 2))


    tank_surface.blit(rotated_body, body_rect.topleft)
    tank_surface.blit(rotated_cannon, cannon_rect.topleft)

    screen.blit(tank_surface, pos)
