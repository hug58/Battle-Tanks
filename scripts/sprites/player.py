
import pygame as pg
import math
from .cannon import Cannon

class Player(Cannon):
    """ This class represents to tank (more cannon) """
    def __init__(self,position):
        self.rect = pg.Rect(position,(30,30)) #get rect in img surface, value init is not used
        self._rect_interno = pg.Rect(0,0,8*2,16*2)
        self._rect_interno.center = self.rect.center
        self._angle = 0
        self._VL = 3
        self.vlx = 0
        self.vly = 0
        self._lifes = 10
        self._dead = False
        self._fire = False
        self._damage = 0
        self._num_player = 0
        Cannon.__init__(self,self.rect.center)

    def update(self):
        """ Update the position of the player and cannon"""   
        self._rect_interno.center = self.rect.center 
        self._rect_cannon.center = self._rect_interno.center
        
    def rotate(self,xbool,angle,surface,rect):
        """ rotate the player around 360"""
        angle +=10*xbool
        if math.sqrt( (angle)**2 ) >= 360:
            angle = 0
        surface = pg.transform.rotate(surface,angle)
        _rect = pg.Rect(rect.topleft,surface.get_size())
        _rect.center = rect.center
        return (angle,_rect)
    
    def _rotate(self,xbool,surface):
        self._angle += 10 * xbool
        angle = math.sqrt(   (self._angle)**2   )
        if angle >= 360:
            self._angle = 0
        surface = pg.transform.rotate(surface,self._angle)
        rect = pg.Rect(self.rect.topleft,surface.get_size())
        rect.center = self.rect.center
        self.rect = rect

    def draw(self,surface,angle):
        return pg.transform.rotate(surface,angle)
    
    @property
    def damage(self):
        """ return damage """
        return self._damage 
    
    
    @property
    def fire(self):
        """ return fire """
        return self._fire
    
    @fire.setter
    def fire(self, value:bool):
        """ setter for fire """
        self._fire = value
        
    @property
    def number_player(self):
        """ get number of player client network """
        return self._num_player