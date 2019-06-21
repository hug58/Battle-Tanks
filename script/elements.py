import pygame as pg
from script import image,sound

class Box(pg.sprite.Sprite):

	def __init__(self,x,y):

		pg.sprite.Sprite.__init__(self)
		self.box_img = image['rect']
		self.image = self.box_img.subsurface((0,0),(42,42))
		self.rect = pg.Rect((x,y),self.image.get_size())

	def update(self):
		pass

class Gun(pg.sprite.Sprite):

	def __init__(self,x,y,game):

		pg.sprite.Sprite.__init__(self,game.objs)
		self.gun_img = image['gun']
		self.image = self.gun_img
		self.rect = pg.Rect((x,y),self.image.get_size())
		self.game = game

	def update(self):

		for sprite in self.game.sprites:
			if self.rect.colliderect(sprite.rect):
				sprite.sprite_powerup('tank_0_gun')
				self.kill()


class Rect(pg.sprite.Sprite):

	def __init__(self,x,y,game,surface):
		pg.sprite.Sprite.__init__(self)
		width = 42
		height = 42
		self.game = game
		self.image = image['rect']
		self.image =  self.image.subsurface((0,42),(width,height))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.rect.x,y= x,y
		surface.blit(self.image,self.rect)



if __name__ == '__main__':
    pass 
