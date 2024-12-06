
""" This is the Player [Tank] """
import math
import pygame as pg
from .cannon import Cannon
from scripts.commons.municion import CannonType



class Player(Cannon):
    """ This class represents to tank (more cannon) """

    SPEED = 3

    def __init__(self,position, cannon_type: CannonType):
        self.rect = pg.Rect(position,(30,30)) #get rect in img surface, value init is not used
        self.body_rect = pg.Rect(0,0,16,16)
        self.body_rect.center = self.rect.center
        self.angle = 0
        self.vl = 3
        self.vlx = 0
        self.vly = 0
        self._life = 10
        self._dead = False
        self._fire = False
        self._damage = 0
        self._num_player = 0
        Cannon.__init__(self,self.rect.center, cannon_type)

    @staticmethod
    def rotate_external(xbool, angle, surface, rect):
        """ rotate the player around 360"""
        angle += 10 * xbool
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

    def draw(self,surface,angle):
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


    @property
    def number_player(self):
        """ get number of player client network """
        return self._num_player
