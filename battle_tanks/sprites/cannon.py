""" GUNS """
import os
import pygame as pg
from ..commons.municion import CannonType


class Cannon:
    """
    Class Cannon, the cannon is object  that can be used to by the player (tank)
    """
    def __init__(self,position,type_gun: CannonType):
        self.rect_cannon = pg.Rect(0,0,20*2,28*2)
        self.rect_cannon.center = position
        # self.image_bullet: pg.Surface = pg.image.load(os.path.join(os.path.abspath("."), "assets/images/bullet"))
        self.angle_cannon = 0
        self.type_gun = type_gun

    def __str__(self):
        return "BULLETS AVAILABLE: " + str(self.type_gun.count_available)

    def check_available_bullets(self):
        """ check available. """
        if self.type_gun.count_available > 0 or self.type_gun.limit is True:
            return True
        return False
