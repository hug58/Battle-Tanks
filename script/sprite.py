import pygame as pg

from script import image,sound
from script.cannon import Cannon
from script.effect import Effect

class Sprite(pg.sprite.Sprite,Cannon):

	def __init__(self,x,y):

		pg.sprite.Sprite.__init__(self)

		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.centery = y
		self.vlx = 0
		self.vly = 0

		self.angle = 0

		self.frames = { 0:(0,0), 1:(0,20), 2:(0,40),}
		self.position = 0
		self.size = (20,20)

		self.effect = pg.sprite.Group()
		self.bullets = pg.sprite.Group()

		Cannon.__init__(self)

		self.gun = False
		self.cont_frame = 0


	def animation(self,delay = 10):
			self.image = self.image_a.subsurface(self.frames[self.position],self.size)
			self.image = pg.transform.scale(self.image,self.size_scale)

			self.cont_frame +=1		
			if self.cont_frame == delay:
				self.position +=1
				self.cont_frame = 0


			if self.position == len(self.frames): 
				self.position = 0

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


	def draw(self,surface):
		for bullet in self.bullets:
			surface.blit(bullet.image,bullet.rect)
		for effect in self.effect:
			surface.blit(effect.image,effect.rect) 

		surface.blit(self.image,self.rect)


	# Por ahora solo cambia la image, ya luego agregaré las funcionalidades 
	def sprite_powerup(self,key_img):
		power_up = Powerup(key_img)
		self.image_a = power_up.image 
		self.gun = power_up.gun


	def dead(self,value):
		#self.image_a = image[f'dead_{value}'] 
		self.image_a = image['dead_{}'.format(value)] 

class Powerup:
	def __init__(self,key_img):
		self.image = image[key_img]
		self.gun = True





if __name__ == '__main__':
	pass 
	