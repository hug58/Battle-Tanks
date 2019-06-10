import pygame as pg
import math


#script
from script import image,sound
from script.sprite import Sprite


class Tank(Sprite):

	def __init__(self,x,y,value = 0):
		#Usado para llevar la cuenta de las vidas en la interface
		self.value = value
		self.value_player()
		
		Sprite.__init__(self,x,y)

		self.angle = 0
		self.move_bool = 0
		self.lifes_all = 10

		self.data = {

			'RIGHT':False,
			'LEFT':False,
			'SPACE':False,
			'UP':False,
			
			'x':200,
			'y':200,

			'angle':0,
			'fire_load':False,
			'player': None,
			'lifes':self.lifes_all,
		}


	def update(self):

		if self.lifes_all == 0:
			self.dead(self.value)
			self.lifes_all = -1

		elif self.lifes_all < 0:
			self.animation()

		elif  -1 < self.lifes_all > 0:	
			self.move()
		
		self.update_cannon()

		self.data['x'] = self.rect.x
		self.data['y'] = self.rect.y
		self.data['fire_load'] = self.load
		self.data['angle'] = self.angle
		self.data['lifes'] = self.lifes_all


	def rotate(self,xbool):
		if xbool == 1:
			self.angle += 90
			if self.angle >= 360: self.angle = 0
		else:
			self.angle -= 90
			if self.angle <= -360: self.angle = 0

		#volver a rotar imagen original
		self.image = self.image_a.subsurface(self.frames[0],
												self.size)
		self.rotate_img()


	def move(self):
		radians = math.radians(self.angle)

		if self.move_bool == 1:
			self.vlx = 3 * - math.sin(radians)
			self.vly = 3 * - math.cos(radians)
	
			self.animation()
			#rotar la animación angulo actual
			self.rotate_img()

		else:
			self.vlx = 0
			self.vly = 0


	def rotate_img(self):
		self.image = pg.transform.scale(self.image,self.size_scale)
		self.image = pg.transform.rotate(self.image,self.angle)


	def value_player(self):
		self.image_a = image[f'tank_{self.value}']
		self.size_scale = (50,50)
		self.image = self.image_a.subsurface((0,0),(20,20))
		self.image = pg.transform.scale(self.image,self.size_scale)

if __name__ == '__main__':
	pass