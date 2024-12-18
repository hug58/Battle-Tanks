import  pygame
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

def create_tank_surface(color: Tuple[int, int, int]) -> pygame.Surface:
    """ Create a new tank surface """
    dark_gray = (64, 64, 64)
    light_gray = (128, 128, 128)
    tank_surface = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
    pygame.draw.rect(tank_surface, color, (10, 4, 12, 24))  # Draw rect green

    # Draw gray rect on the sides, adjusted to connect with the green part
    pygame.draw.rect(tank_surface, dark_gray, (4, 4, 6, 24), border_radius=2)  # Left
    pygame.draw.rect(tank_surface, dark_gray, (22, 4, 6, 24), border_radius=2)  # Right

    # Adjust the position of the wheels to connect with the green part
    for i in range(4, 24, 4):
        pygame.draw.rect(tank_surface, light_gray, (4, i + 2, 6, 2), border_radius=1)  # Left
        pygame.draw.rect(tank_surface, light_gray, (22, i + 2, 6, 2), border_radius=1)  # Right

    return tank_surface


def darken_color(color: Tuple[int, int, int], factor: float = 0.2) -> Tuple[int, int, int]:
    """Returns a darker color based on the original color."""
    return (
        max(0, int(color[0] * (1 - factor))),
        max(0, int(color[1] * (1 - factor))),
        max(0, int(color[2] * (1 - factor)))
    )



def create_cannon_surface(color: Tuple[int, int, int]) -> pygame.Surface:
    DARK_GREEN_LOCAL = darken_color(color)
    LIGHT_GREEN_LOCAL = darken_color(color, factor=0.1)
    cannon_surface = pygame.Surface((20, 28), pygame.SRCALPHA)
    pygame.draw.rect(cannon_surface, DARK_GREEN_LOCAL, (0, 12, 20, 16))
    pygame.draw.rect(cannon_surface, LIGHT_GREEN_LOCAL, (4, 4, 12, 12))
    pygame.draw.rect(cannon_surface, YELLOW, (8, 8, 4, 4))
    pygame.draw.rect(cannon_surface, LIGHT_GREEN, (8, 0, 4, 8))

    return cannon_surface
