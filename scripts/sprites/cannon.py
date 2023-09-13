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