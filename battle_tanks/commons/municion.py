
""" MANAGEMENT OF THE MUNICION """

from typing import  List,Tuple
import pygame as pg
from battle_tanks.commons.tank_surface import draw_bullet

class CannonType:
    """ MANAGEMENT OF THE MUNICION """
    def __init__(self,count,gun_type, size:Tuple[int,int]):
        self.count = count
        self._count_available = count
        self.type:dict = gun_type
        self.limit = False
        self.vl = None
        self.size = size
        self.damage = None
        self._reload_time = 100
        self._count_reload = 0


    @property
    def count_available(self):
        """ check count available """
        return self._count_available


    @count_available.setter
    def count_available(self, count_available):
        """ check count available """
        self._count_available = count_available


    def render(self, bullet_surface: pg.Surface) -> pg.Surface:
        """ getting bullets surfaces """
        width = self.size[0]
        bullets = [ (width*i,0) for i in range(0,self._count_available)]

        if self._count_available <= 0:
            self._count_reload +=1

        if self._count_available <= 0 and self._count_reload >= self._reload_time:
            self._count_reload = 0
            self._count_available = self.count


        for bullet in bullets:
            draw_bullet(bullet_surface, bullet, 0, (4,10))

        return bullet_surface
