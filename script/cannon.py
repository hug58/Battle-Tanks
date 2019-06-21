import pygame as pg
import math

from script import image,sound
from script.effect import Effect

class Bala(pg.sprite.Sprite):
	def __init__(self,point,angle,value,effect):
		
		pg.sprite.Sprite.__init__(self)
		self.image_b = image['bullet_{}'.format(value)]
		self.image = pg.transform.rotate(self.image_b,angle)
		self.rect = self.image.get_rect()
		radians = math.radians(angle)
		self.rect.x = point[0] + (2 * math.sin(radians)) - self.rect.width//2 
		self.rect.y = point[1] + (2 * math.cos(radians)) - self.rect.height //2
		
		self.vlx = -10 * math.sin(radians)
		self.vly = -10 * math.cos(radians)
	
		self.angle = angle
		self.effect = effect

	def update(self):
		#Eliminar balas que chocan entre si
			
		self.rect.x +=self.vlx
		self.rect.y += self.vly

	def explosion(self):
		frames = {
			0:(0,0),
			1:(0,14),
			2:(0,28),
			3:(0,42),
		}
		self.point_ball = ((self.rect.centerx,self.rect.centery))

		effect = Effect(self.point_ball,
						self.angle,
						frames,(14,14),
						image['explosion'])

		self.effect.add(effect)
		
		self.kill()


class Cannon:
	def __init__(self):
		self.cont = 30
		self.fire = False
		self.load = False

		self.effect_frames  = {
				0:(0,0),
				1:(0,15),
				2:(0,30),
				3:(0,45),
				4:(0,60),
			}

	def update_cannon(self,automatico = False):
		
		self.effect.update()
		self.bullets.update()

		if self.gun != True:

			limit = 40

			if self.cont < 40: 
				self.cont +=1
				self.fire = False
			else: 
				self.load = True
		
		#Arma 2 con tiempo de cargar menor

		else:
			limit = 10
			if self.cont < limit: 
				self.cont +=1
				self.fire = False
			else: 
				self.load = True

		if (self.fire == True and self.cont >= 10 
			or automatico == True and self.cont >= 40):
			
			# Codigo cutre, lo voy a mejorar pronto, lo prometo.
			#bueno tal vez no xD.
			#Bueno, medio lo hice, por ahora no importa mucho
			
			if self.gun != True:
				self.queue_shot(1)
			else:
				self.queue_shot(2)

	def queue_shot(self,queue):
		pos_gun = 0
		for i in range(queue):

			if queue > 1:
				if i == 0:
					pos_gun -= 10
				elif i > 0:
					pos_gun +=20

			self.point_ball = ((self.rect.centerx - 
								pos_gun,
								self.rect.centery-pos_gun))
			
			sound['shot'].stop()
			sound['shot'].play()
			
			self.effect.add(Effect(self.point_ball,
										self.angle,
										self.effect_frames,
										(16,15),image['wave_shot']))

			self.bullets.add(Bala(self.point_ball,
										self.angle,
										self.value,
										self.effect
										))


		self.load = False
		self.cont = 0

if __name__ == '__main__':
	pass 
