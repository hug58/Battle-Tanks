
from script import * 
from script.sprite import Sprite

class Tank(Sprite):

	def __init__(self,x,y,game,value = 0):
		self.value = value
		self.image_a = image["tank_{}".format(value)]
		self.size_scale = (50,50)
		self.image = self.image_a.subsurface((0,0),(20,20))
		self.image = pg.transform.scale(self.image,self.size_scale)
		#self.image = pg.transform.scale(self.image_a.subsurface((0,0),(20,20)),self.size_scale)
		Sprite.__init__(self,x,y,game)

		if  pg.joystick.get_count() > 0 and  pg.joystick.get_count() < 2 and value == 0: self.joystick =  pg.joystick.Joystick(value)
		elif pg.joystick.get_count() > 1 and value == 1: self.joystick =  pg.joystick.Joystick(value)
		else: self.joystick =  None
	
		if self.joystick != None: self.joystick.init()
	
		self.angle = 0
		self.move_bool = 0
		self.vidas = 3

		self.teclas = {

			'RIGHT':False,
			'LEFT':False,
			'SPACE':False,
			'UP':False,
			
			'x':200,
			'y':200,

			'angle':0,
			'fire_load':False

		}


	def update(self):

		self.move()

		self.collided()
		self.cannon.update()

		for shot in self.game.bullets:
			if shot.rect.colliderect(self.rect):
				if shot.value != self.value:
					self.vidas -=1
					shot.explosion()
					self.game.bullets.remove(shot)

		
		self.teclas['x'] = self.rect.x
		self.teclas['y'] = self.rect.y
		self.teclas['fire_load'] = self.cannon.load
		self.teclas['angle'] = self.angle
		
	def rotate(self,xbool):


		if xbool == 1:
			self.angle += 90
			if self.angle >= 360: self.angle = 0
		else:
			self.angle -= 90
			if self.angle <= -360: self.angle = 0
		
		self.image = self.image_a.subsurface(self.frames[0],self.size)
		
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

if __name__ == '__main__':
	print("Este programa es independiente")
else:
	print("El modulo {name} ha sido importado".format(name = __name__))