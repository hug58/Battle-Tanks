import pygame as pg
import math

class Cannon:
    """ 
    Class Cannon, the cannon is object  that can be used to by the player (tank)
    """ 
    def __init__(self,position):
        self._rect_cannon = pg.Rect(0,0,20*2,28*2)
        self._rect_cannon.center = position
        self._angle_cannon = 0 
        
    def rotate(self,xbool,angle,surface,rect):
        """ rotate cannon around 360 """
        angle +=10*xbool
        if math.sqrt( (angle)**2 ) >= 360:
            angle = 0
        surface = pg.transform.rotate(surface,angle)
        _rect = pg.Rect(rect.topleft,surface.get_size())
        _rect.center = rect.center
        return (angle,_rect)