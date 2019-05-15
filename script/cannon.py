#import math 
#import pygame as pg

from script.effect import Effect
from script import *

class Bala(pg.sprite.Sprite):

	def __init__(self,point,angle,value,game):
		
		pg.sprite.Sprite.__init__(self)
		self.image_b = image["bullet_{}".format(value)]
		self.image = pg.transform.rotate(self.image_b,angle)
		self.rect = self.image.get_rect()
		self.game = game
		radians = math.radians(angle)
		self.rect.x = point[0] + (2 * math.sin(radians)) - self.rect.width//2 
		self.rect.y = point[1] + (2 * math.cos(radians)) - self.rect.height //2
		
		self.vlx = -10 * math.sin(radians)
		self.vly = -10 * math.cos(radians)
	
		self.value = value
		self.angle = angle

	def update(self):
		
		if  (0 > self.rect.x or self.rect.x > self.game.WIDTH 
			or  0 > self.rect.y or self.rect.y > self.game.HEIGHT): 
			self.kill() 


		#Eliminar balas que chocan entre si

		for bullet in self.game.bullets:
			if bullet.value  != self.value:
				if self.rect.colliderect(bullet.rect): 
					self.game.bullets.remove(bullet)
					self.kill()


		# collided Rect--bals
		#collided Box-balls#
		if (pg.sprite.spritecollide(self,self.game.obs,0) 
		or pg.sprite.spritecollide(self,self.game.objs,0)): 
			self.explosion()
			
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
						image["explosion"])

		self.game.effect.add(effect)
		
		self.kill()

class Cannon:
	def __init__(self,game,sprite):
		self.cont = 30
		self.game = game
		self.fire = False
		self.load = False

		self.sprite = sprite
		self.effect_frames  = {
				0:(0,0),
				1:(0,15),
				2:(0,30),
				3:(0,45),
				4:(0,60),
			}

	def update(self,automatico = False):
		
		if self.sprite.gun != True:

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

			if self.sprite.gun != True:
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



			self.point_ball = ((self.sprite.rect.centerx - 
								pos_gun,
								self.sprite.rect.centery-pos_gun))
			
			sound["shot"].stop()
			sound["shot"].play()
			
			self.game.effect.add(Effect(self.point_ball,
										self.sprite.angle,
										self.effect_frames,
										(16,15),image["wave_shot"]))

			self.game.bullets.add(Bala(self.point_ball,
										self.sprite.angle,
										self.sprite.value,
										self.game))


		self.load = False
		self.cont = 0


if __name__ == '__main__':
    print("Este programa es independiente")
else:
    print("El modulo {name} ha sido importado".format(name = __name__))