import pygame as pg
from scripts import ROUTE

class Brick(pg.sprite.Sprite):
    """Class representing a Brick object"""
    def __init__(self,x_pos,y_pos,width,height):
        pg.sprite.Sprite.__init__(self)
        self.box_img = pg.image.load(ROUTE("ASSETS/images/tiles.png"))
        self.image = self.box_img.subsurface((0,0),(32,32))
        self.rect = pg.Rect((x_pos,y_pos),(width,height))


class Block(pg.sprite.Sprite):
    """ Class representing a Block object """
    def __init__(self,x_pos,y_pos,width,height):
        pg.sprite.Sprite.__init__(self)
        self.rect = pg.Rect((x_pos,y_pos),(width,height))