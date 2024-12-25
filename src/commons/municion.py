
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


    def render(self) -> List:
        """ getting bullets surfaces """
        witdh = self.size[0]

        if self._count_available <= 0:
            self._count_realod +=1

        if self._count_available <= 0 and self._count_realod >= self._reload_time:
            self._count_realod = 0
            self._count_available = self.count


        bullets = [(self.type, (witdh*i,0)) for i in range(0,self._count_available)]
        return bullets
