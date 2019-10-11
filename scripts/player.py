import pygame as pg
import math

from scripts import ROUTE

class Animation:
	def __init__(self,image,frames):
		
		self._frames = frames
		self._current_frame = 0

		self._image = image
		#self.image = self._image.subsurface(self._frames[self._current_frame])
		
		self._delay = 4
		self._cont = 0
		self._done = False

	def _update(self):
			
		self.image = self._image.subsurface(self._frames[self._current_frame])

		self._cont +=1		
		if self._cont == self._delay:
			self._current_frame +=1
			self._cont = 0

		if self._current_frame == len(self._frames): 
			self._done =True

class Cannon:
	def __init__(self,position):
		self._rect_cannon = pg.Rect(0,0,20*2,28*2)
		self._rect_cannon.center = position
		self._angle_cannon = 0 



class Bullet(pg.sprite.Sprite,Animation):

	def __init__(self,position,angle,num_player):

		pg.sprite.Sprite.__init__(self)

		explosion = pg.image.load(ROUTE(f'ASSETS/images/explosion_bullet_0{num_player}.png'))
		explosion = pg.transform.scale(explosion,(16,48))
		size_e = (16,16)
		frames = {0:((0,0),size_e),1:((0,16),size_e),2:((0,32),size_e)}
		Animation.__init__(self,explosion,frames)


		self.image = pg.Surface((4,8))
		self.image.fill((2,218,136)) if num_player == 0 else self.image.fill((188,2,218))
		self.image = pg.transform.rotate(self.image,angle)

		self.rect = self.image.get_rect()
		self._VL = 20

		self.rect.center = position


		self.radians = math.radians(angle)


		self.rect.centerx +=  math.sin(self.radians) * -30 
		self.rect.centery +=  math.cos(self.radians) * -30


		self.vlx = self._VL * - math.sin(self.radians)
		self.vly = self._VL * - math.cos(self.radians)

		self.explosion = False 

		self._num_player = num_player


		self._delay = 2


	def update(self):


		if self.explosion != True:
			self.rect.centerx += self.vlx
			self.rect.centery += self.vly

		else:
			self._update()

			rect = self.image.get_rect()
			rect.center = self.rect.center
			self.rect = rect

			if self._done:
				self.kill()


	def draw(self,SCREEN):

		SCREEN.blit(self.image,self.rect)


class Player(Cannon):

	def __init__(self,position):

		self.rect = pg.Rect(position,(64,64))

		self._rect_interno = pg.Rect(0,0,40,40)
		self._rect_interno.center = self.rect.center

		self._angle = 0
		self._VL = 12
		self.vlx = 0
		self.vly = 0

		self._lifes = 10
		self._dead = False
		self._fire = False
		self._damage = 0


		self._num_player = 0


		Cannon.__init__(self,self.rect.center)


	def update(self):
		self._rect_interno.center = self.rect.center 
		self._rect_cannon.center = self._rect_interno.center


	def rotate(self,xbool,angle,surface,rect):

		angle +=10*xbool

		if math.sqrt( (angle)**2 ) >= 360:
			angle = 0


		surface = pg.transform.rotate(surface,angle)
		_rect = pg.Rect(rect.topleft,surface.get_size())
		_rect.center = rect.center

		return (angle,_rect)



	def _rotate(self,xbool,surface):
		
		self._angle += 10 * xbool

		angle = math.sqrt(   (self._angle)**2   )
		#print(self._angle)
		if angle >= 360:
			self._angle = 0

	

		surface = pg.transform.rotate(surface,self._angle)

		rect = pg.Rect(self.rect.topleft,surface.get_size())
		rect.center = self.rect.center
		self.rect = rect


	def _draw(self,surface,angle):
		return pg.transform.rotate(surface,angle)
