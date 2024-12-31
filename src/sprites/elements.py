import pygame as pg
from src import ROUTE, sound_boom

class Brick(pg.sprite.Sprite):
    """Class representing a Brick object"""
    def __init__(self,x_pos,y_pos,width,height):
        super().__init__()
        self.box_img = pg.image.load(ROUTE("assets/images/tiles.png"))
        self.image = self.box_img.subsurface((0,0),(32,32))
        self.rect = pg.Rect((x_pos,y_pos),(width,height))
        self._data = None

    @staticmethod
    def boom():
        """C BOOM"""
        sound_boom.play()

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data:bytes):
        self._data = data


class Block(pg.sprite.Sprite):
    """ Class representing a Block object """
    def __init__(self,x_pos,y_pos,width,height):
        super().__init__()
        self.rect = pg.Rect((x_pos,y_pos),(width,height))