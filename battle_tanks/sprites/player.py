""" This is the Player [Tank] """
import math
import os
import pygame as pg
from .cannon import Cannon
from battle_tanks.commons.municion import CannonType

from typing import Callable


class Player(Cannon):
    """ This class represents to tank (more cannon) """
    SPEED = 2
    ANGLE = 5
    ANGLE_RIGHT = 1
    ANGLE_LEFT = -1
    SIZE_BODY_RECT = (32,32)
    DAMAGE =  10
    MAX_DAMAGE = 100


    TELESCOPIC_SIGH = pg.image.load(os.path.join(os.path.abspath("."), "assets/images/telescopic_sight.png"))
     

    def __init__(self, position: tuple, number: int, cannon_type: dict):
        super().__init__(position, cannon_type)
        self.player_number = number
        self.name = f"Player {number}"  # Nombre por defecto
        self.damage = 0
        self.fire = False
        self.angle = 0
        self.angle_cannon = 0
        self.type_gun = cannon_type

        self.image = pg.Surface((32, 32), pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

        self.body_rect = pg.Rect(0, 0, 32, 32)
        self.body_rect.center = self.rect.center

        self.vl = 3
        self.vlx = 0
        self.vly = 0
        self._life = 10
        self._dead = False


    @staticmethod
    def rotate_external(xbool, angle, surface, rect):
        """ rotate the player around 360"""
        angle += Player.ANGLE * xbool
        if math.sqrt(angle ** 2) >= 360:
            angle = 0
        surface = pg.transform.rotate(surface, angle)
        rect = pg.Rect(rect.topleft, surface.get_size())
        rect.center = rect.center
        return angle, rect


    def update(self):
        """ Update the position of the player and cannon"""   
        self.body_rect.center = self.rect.center
        self.rect_cannon.center = self.body_rect.center


    def rotate_rect(self,xbool,surface):
        """Rotate the rect player around"""
        self.angle += 10 * xbool
        angle = math.sqrt(self.angle**2)
        if angle >= 360:
            self.angle = 0
        surface = pg.transform.rotate(surface,self.angle)
        rect = pg.Rect(self.rect.topleft,surface.get_size())
        rect.center = self.rect.center
        self.rect = rect


    @staticmethod
    def draw(surface,angle):
        """ Draw the surface """
        return pg.transform.rotate(surface,angle)


    @property
    def damage(self):
        """ return damage """
        return self._damage


    @damage.setter
    def damage(self, value:float):
        """setter for damage"""
        self._damage = value


    @property
    def fire(self):
        """ return fire """
        return self._fire


    @fire.setter
    def fire(self, value:bool):
        """ setter for fire """
        self._fire = value
        if self._fire is True:
            self.type_gun.count_available -=1


    def telescopic_sight(self):
        """ Draw the telescopic sight """
        return {
                "x": self.rect.x,
                "y": self.rect.y,
                "angle_cannon": self.angle_cannon,
        }
        



    def __str__(self):
        return f"---NUMBER: [{self.player_number}  ---POS: [{self.rect.center}] ---DAMAGE: {self._damage}"
