

from script import *
from script.sprite import Sprite

class Enemy(Sprite):

	def __init__(self,x,y,game):
		#self.size_scale = (50,50)
		self.image_a = game.images["tank_1"]
		self.size_scale = (50,50)

		self.image = self.image_a.subsurface((0,0),(20,20))
		self.image = pg.transform.scale(self.image,self.size_scale)

		Sprite.__init__(self,x,y,game)
		self.angle = 0
		self.value = 1

	def update(self):

		for shot in self.game.bullets:
			if shot.rect.colliderect(self.rect):
				if shot.value != self.value:
					shot.explosion()
					self.kill()


		self.animation()
		self.move()
		self.collided()
		self.cannon.update(True)


		#Prueba del modo gun
		self.gun = False

	def move(self):

		self.distance_x = math.sqrt((self.rect.centerx - self.game.player.rect.centerx)**2)
		self.distance_y = math.sqrt((self.rect.centery - self.game.player.rect.centery)**2)

		if self.distance_x > 0:
			self.vly = 0
			if self.game.player.rect.left < self.rect.left: self.vlx = -2
			elif self.game.player.rect.right > self.rect.right: self.vlx = 2

		elif self.distance_x <= 0:
			self.vlx = 0
			if self.game.player.rect.top > self.rect.top: self.vly = 2
			elif  self.game.player.rect.bottom < self.rect.bottom: self.vly = -2

		if self.vlx > 0: self.angle = -90
		elif self.vlx < 0: self.angle = 90
		if self.vly > 0: self.angle = 180
		elif self.vly < 0: self.angle = 0

		self.image = pg.transform.rotate(self.image,self.angle)
		#self.image = pg.transform.scale(self.image,self.size_scale)



if __name__ == '__main__':
    print("Este programa es independiente")
else:
    print("El modulo {name} ha sido importado".format(name = __name__))