import pygame as pg

from scripts import ROUTE

class Brick(pg.sprite.Sprite):

	def __init__(self,x,y,width,height):

		pg.sprite.Sprite.__init__(self)

		self.box_img = pg.image.load(ROUTE("ASSETS/images/tiles.png"))
		self.image = self.box_img.subsurface((0,0),(32,32))
		self.rect = pg.Rect((x,y),(width,height))



class Block(pg.sprite.Sprite):

	def __init__(self,x,y,width,height):
		pg.sprite.Sprite.__init__(self)
		self.rect = pg.Rect((x,y),(width,height))



if __name__ == '__main__':
    pass 
