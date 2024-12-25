
""" MANAGEMENT OF THE MUNICION """

from typing import Dict, List, Tuple

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


    def render(self) -> List:
        """ getting bullets surfaces """
        width = self.size[0]

        if self._count_available <= 0:
            self._count_reload +=1

        if self._count_available <= 0 and self._count_reload >= self._reload_time:
            self._count_reload = 0
            self._count_available = self.count


        bullets = [(self.type, (width*i,0)) for i in range(0,self._count_available)]
        return bullets
