import  pygame
from typing import Tuple

BLACK = (7, 6, 0)
RED = (234, 82, 111)
WHITE = (247,247, 255)
BLUE = (39, 154, 241)

colors = {
    0: BLUE,
    1: RED,
    2: WHITE,
    3: BLACK
}

def create_tank_surface(color: Tuple[int, int, int]) -> pygame.Surface:
    """ Create a new tank surface """
    dark_gray = (64, 64, 64)
    light_gray = (128, 128, 128)
    tank_surface = pygame.Surface((32, 32), pygame.SRCALPHA,
                                  32)
    pygame.draw.rect(tank_surface, color, (10, 4, 12, 24))  # Draw rect green

    # Draw gray rect on the sides, adjusted to connect with the green part
    pygame.draw.rect(tank_surface, dark_gray, (4, 4, 6, 24), border_radius=2)  # Left
    pygame.draw.rect(tank_surface, dark_gray, (22, 4, 6, 24), border_radius=2)  # Right

    # Adjust the position of the wheels to connect with the green part
    for i in range(4, 24, 4):
        pygame.draw.rect(tank_surface, light_gray, (4, i + 2, 6, 2), border_radius=1)  # Left
        pygame.draw.rect(tank_surface, light_gray, (22, i + 2, 6, 2), border_radius=1)  # Right

    return tank_surface

