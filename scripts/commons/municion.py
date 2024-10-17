
""" MANAGEMENT OF THE MUNICION """

import pygame as pg
from typing import Tuple, List

class CannonType:
    """ MANAGEMENT OF THE MUNICION """
    def __init__(self,count,gun_type:pg.Surface):
        self.count = count
        self._count_available = count
        self.type:pg.Surface = gun_type
        self.limit = False
        self.vl = None
        self.damage = None
        self._reload_time = 100
        self._count_realod = 0




    @property
    def count_available(self):
        """ check count available """
        return self._count_available


    @count_available.setter
    def count_available(self, count_available):
        """ check count available """
        print(f"Count available: {self._count_available}")
        self._count_available = count_available


    def render(self) -> List[pg.Surface]:
        """ getting bullets surfaces """
        witdh = self.type.get_rect().right

        if self._count_available <= 0:
            self._count_realod +=1

        if (self._count_available <= 0 and self._count_realod >= self._reload_time):
            self._count_realod = 0
            self._count_available = self.count


        bullets = [(self.type, (witdh*i,0)) for i in range(0,self._count_available)]
        return bullets
