
from script import *
from script.cannon import Cannon


class Sprite(pg.sprite.Sprite):

	def __init__(self,x,y,game):

		pg.sprite.Sprite.__init__(self)
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.centery = y
		self.vlx = 0
		self.vly = 0

		self.angle = 0
		self.game = game

		self.cannon = Cannon(self.game,self)

		self.frames = { 0:(0,0), 1:(0,20), 2:(0,40),}
		self.position = 0
		self.size = (20,20)


		self.gun = False

	def collided(self):

		if self.rect.right >= self.game.WIDTH: self.rect.right = self.game.WIDTH
		elif self.rect.left <= 0: self.rect.left = 0

		if self.rect.bottom >= self.game.HEIGHT: self.rect.bottom = self.game.HEIGHT
		elif self.rect.top <= 0: self.rect.top = 0

		self.rect.centerx += self.vlx

		self.collided_group((1,0),self.game.sprites)
		self.collided_group((1,0),self.game.obs)
		self.collided_group((1,0),self.game.enemies)


		self.rect.centery += self.vly

		self.collided_group((0,1),self.game.sprites)
		self.collided_group((0,1),self.game.obs)
		self.collided_group((0,1),self.game.enemies)


	def animation(self):

			self.image = self.image_a.subsurface(self.frames[self.position],self.size)
			self.image = pg.transform.scale(self.image,self.size_scale)

			#self.image = pg.transform.scale(self.image,self.size_scale)
			self.position +=1
			if self.position >= len(self.frames): self.position = 0


	def collided_group(self,posxy,group):
		for rect in group:
			if self.rect != rect:
				if self.rect.colliderect(rect.rect):

					if posxy == (1,0):

						if self.vlx > 0: self.rect.right = rect.rect.left
						elif self.vlx < 0: self.rect.left = rect.rect.right

					else:

						if self.vly >= 0:
							self.rect.bottom = rect.rect.top
							self.vly = 0
						elif self.vly < 0: self.rect.top = rect.rect.bottom


	# Por ahora solo cambia la image, ya luego agregaré las funcionalidades 

	def sprite_powerup(self,key_img):
		power_up = Powerup(key_img)
		self.image_a = power_up.image 
		self.gun = power_up.gun


class Powerup:
	def __init__(self,key_img):
		self.image = image[key_img]
		self.gun = True





if __name__ == '__main__':
    print("Este programa es independiente")
else:
    print("El modulo {name} ha sido importado".format(name = __name__))