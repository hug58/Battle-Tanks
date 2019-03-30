"""

	Hecho por hug58


	Ideas: bombas, difrentes formas de disparo, y escudos

"""


import random,os,sys,math,socket
import pygame as pg

pg.display.init()
pg.mixer.init()
pg.joystick.init()


#__CONSTANS__#
SPACEMAP = 42
lvl_0 = [
			"11111111111111111111111",
			"10000000000000000000001",
			"10000000000000000000001",			
			"10000000000000000000001",
			"10011000111110030110001",
			"10011000102011000110001",
			"10000000000000000000001",
			"10000000000000000000001",
			"10000000000000000000001",
			"10400000000000000000001",
			"10000000000000000000001",
			"11111111111111111111111",
		]
lvl_map = {
	"lvl_0":lvl_0,
}

def resolve_route(route_relative):
	if hasattr(sys,"_MEIPASS"):
		return os.path.join(sys._MEIPASS,route_relative)

	return os.path.join(os.path.abspath("."),route_relative)

def collide(point,rect):
	collided=0
	if point[0]>=rect[0] and point[0]<rect[0]+rect[2] \
	and point[1]>=rect[1] and point[1]<rect[1]+rect[3]:
		collided=1
	return collided
   
def rect_collision(rect1,rect2):
	collision=0
	point1=(rect1[0],rect1[1])
	point2=(rect1[0]+rect1[2],rect1[1])
	point3=(rect1[0],rect1[1]+rect1[3])
	point4=(rect1[0]+rect1[2],rect1[1]+rect1[3])

	
	if collide(point1,rect2) or collide(point2,rect2) \
	or collide(point3,rect2) or collide(point4,rect2):
	   collision=1
	return collision

def rect_group(rect2,group):
	for obs in group:
		if rect_collision(obs.rect,rect2):
			return 1

image = {	
			"tank_0":pg.image.load(resolve_route("image/limonero_tank.png")),
			"tank_1":pg.image.load(resolve_route("image/uvadero_tank.png")),
			
			"bullet_0":pg.image.load(resolve_route("image/bullet_a.png")),
			"bullet_1":pg.image.load(resolve_route("image/bullet_e.png")),
			"Rect":pg.image.load(resolve_route("image/Rect.png")),
			"Box":pg.image.load(resolve_route("image/box.png")),
			"wave_shot" : pg.image.load("image/effect_shot.png")
}

sound = { 
			"shot":pg.mixer.Sound(resolve_route("sound/shot.wav")),	
			"box":pg.mixer.Sound(resolve_route("sound/box.wav")),
}

pg.display.set_icon(image["tank_0"])

class Life:
	def __init__(self,x,y,value):
		self.image = image[f"tank_{value}"]
		self.x = x
		self.y = y 

class Tablero:
	def __init__(self,game):
		self.game = game
		self.image = pg.Surface((self.game.WIDTH,42))
		
		self.vidas_player_1 = [ Life(40*(i+1),0,0) for i in range(3)]
		self.vidas_player_2 = [Life(782 + 42*(i+1),0,1) for i in range(3)]
		self.make_tablero(self.image)

	def update(self):
		for sprites in self.game.sprites:
			if sprites.value == 0:

				if len(self.vidas_player_1) > 0:

					if sprites.vidas < len(self.vidas_player_1) or sprites.vidas > len(self.vidas_player_1):
						if sprites.vidas < len(self.vidas_player_1):
							self.vidas_player_1.pop()
						elif sprites.vidas > len(self.vidas_player_1):
							posx = self.vidas_player_1[-1].x
							self.vidas_player_1.append(Life(posx + 42 ,0,0))
						
						self.make_tablero(self.image)

				else:
					print(f"Jugador {sprites.value + 1 } Perdió!")

			if sprites.value == 1:

				if len(self.vidas_player_2) > 0:
				
					if sprites.vidas < len(self.vidas_player_2) or sprites.vidas > len(self.vidas_player_2):
						if sprites.vidas < len(self.vidas_player_2):
							self.vidas_player_2.pop()
						elif sprites.vidas > len(self.vidas_player_2):
							posx = self.vidas_player_2[-1].x
							self.vidas_player_2.append(Life(posx + 42 ,0,1))

						self.make_tablero(self.image)

				else:
					print(f"Jugador {sprites.value + 1 } Perdió!")

	def make_tablero(self,surface):

		self.image.fill(pg.Color("#04441C"))

		for vidas in self.vidas_player_1:
			surface.blit(vidas.image,(vidas.x,vidas.y))
		for vidas in self.vidas_player_2:
			surface.blit(vidas.image,(vidas.x,vidas.y))




	def draw(self,SCREEN):
		SCREEN.blit(self.image,(0,self.game.HEIGHT))

class Mission:
	def __init__(self,game):
		self.game = game
		self.objetivos = {"lvl_0": self.All_kill,}
		self.mission_actual = self.objetivos[self.game.lvl]

	def update(self):
		self.mission_actual()
		if self.mission_actual() == True:
			print("¡Mission COMPLET!")

	def All_kill(self):
		if len(self.game.enemies) > 0:
			return False
		else:
			return True

class Animation:
	
	def __init__(self,frames):
		self.current_frames = 0
		self.limit = len(frames)
		self.step = 15
		self.cont = 0
		
	def update(self,condition):
		
		if self.cont >= self.step:			
			if self.current_frames < self.limit:
				self.current_frames +=1
			if self.current_frames == self.limit:
				self.current_frames = 0 if condition == 1 else self.current_frames
				
			self.cont = 0
		elif self.cont == 0:
			self.current_frames = 0

		self.cont +=1

class Box(pg.sprite.Sprite):

	def __init__(self,x,y,game):

		pg.sprite.Sprite.__init__(self)
		self.box_img = image["Box"]
		self.image = self.box_img.subsurface((10,0),(10,10))
		self.image = pg.transform.scale(self.image,(30,30))
		self.rect = pg.Rect((x,y),self.image.get_size())
		
		self.frames = {
			0:(0,0),
			1:(10,0),
		}

		self.animation = Animation(self.frames)
		self.game = game

	def update(self):

		frame = self.animation.current_frames
		self.animation.update(1)
		self.image = self.box_img.subsurface(self.frames[frame],(10,10))
		self.image = pg.transform.scale(self.image,(30,30))
		
		for sprites in self.game.sprites:
			if self.rect.colliderect(sprites.rect):
				self.kill()
				sound["box"].play

class Effect(pg.sprite.Sprite):
	def __init__(self,pos,angle):

		pg.sprite.Sprite.__init__(self)
		self.effect = image["wave_shot"]
		self.image = self.effect.subsurface((0,0),(17,17))
		self.image = pg.transform.scale(self.image,(17*2,17*2))
		self.rect = self.image.get_rect()

		self.radians = math.radians(angle)		
		self.rect.x = (pos[0] - (20 * math.sin(self.radians))) - self.rect.width//2 
		self.rect.y = pos[1] - (20 * math.cos(self.radians)) - self.rect.height //2
		
		self.pos = pos
		self.frames = {
			0:(0,0),
			1:(0,17),
			2:(0,34),
			3:(0,51),
			4:(0,68),
		}

		self.animation = Animation(self.frames)
		self.animation.step = 2
		self.pos = pos

	def update(self):

		frame = self.animation.current_frames
		self.animation.update(0)
		self.image = self.effect.subsurface(self.frames[frame],(17,17))
		self.image = pg.transform.scale(self.image,(17*2,17*2))


		if self.animation.current_frames >= len(self.frames):
			self.kill()

		self.rect.x = self.pos[0] - (20 * math.sin(self.radians)) - self.rect.width//2 
		self.rect.y = self.pos[1] - (20 * math.cos(self.radians)) - self.rect.height //2

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

	def update(self):
		
		if  0 > self.rect.x or self.rect.x > self.game.WIDTH or  0 > self.rect.y or self.rect.y > self.game.HEIGHT:
			self.kill() 

		# collided Rect--bals
		self.kill() if pg.sprite.spritecollide(self,self.game.obs,0) else None
		#collided Box-balls#
		self.kill() if pg.sprite.spritecollide(self,self.game.objs,0) else None

		self.rect.x +=self.vlx
		self.rect.y += self.vly

class Sprite(pg.sprite.Sprite):
	
	def __init__(self,x,y,game):

		pg.sprite.Sprite.__init__(self)
		self.rect = self.image.get_rect()
		#self.rect = pg.Rect((x,y),(45,40))
		self.rect.x = x
		self.rect.y = y
		self.vlx = 0
		self.vly = 0
		
		self.angle = 0		
		self.game = game
		self.effect = []


	def cannon(self,fire):
		self.point_ball = ((self.rect.centerx,self.rect.centery))
		if fire == True:

			sound["shot"].stop()
			sound["shot"].play()
			self.game.effect.add(Effect(self.point_ball,self.angle))
			self.game.bullets.add(Bala(self.point_ball,self.angle,self.value,self.game))

	def collided(self):
	
		if self.rect.right >= self.game.WIDTH:
			self.rect.right = self.game.WIDTH
		elif self.rect.left <= 0:
			self.rect.left = 0

		if self.rect.bottom >= self.game.HEIGHT:
			self.rect.bottom = self.game.HEIGHT
		elif self.rect.top <= 0:
			self.rect.top = 0

		self.rect.x += self.vlx
		colision = pg.sprite.spritecollide(self,self.game.obs,0)
		
		for block in colision:
			if self.vlx > 0:
				#self.cont_jump = 1
				self.rect.right = block.rect.left
			elif self.vlx < 0:
				#self.cont_jump = 1
				self.rect.left = block.rect.right

		self.rect.y +=self.vly
		colision = pg.sprite.spritecollide(self,self.game.obs,0)
		
		for block in colision:
			if self.vly >= 0:
				self.rect.bottom = block.rect.top
				self.vly = 0

			elif self.vly < 0:
				self.rect.top = block.rect.bottom

class Enemy(Sprite):
	
	def __init__(self,x,y,game):
		self.image_e = image["tank_1"]
		self.image = pg.transform.scale(self.image_e,(40,40))
		Sprite.__init__(self,x,y,game)		
		self.angle = 0
		self.value = 1

		self.cont_shot = 0 

	def update(self):
		
		for shot in self.game.bullets:
			if shot.rect.colliderect(self.rect):
				if shot.value != self.value:
					self.kill()

		self.move()
		self.collided()
		self.shot()

	def move(self):
		
		colision = rect_group(self.rect ,self.game.obs)
		
		self.distance_x = math.sqrt((self.rect.centerx - self.game.player.rect.centerx)**2)
		self.distance_y = math.sqrt((self.rect.centery - self.game.player.rect.centery)**2)


		if self.distance_x > 0 or colision == 1:
		
			self.vly = 0
			if self.game.player.rect.left < self.rect.left:
				self.vlx = -2
			elif self.game.player.rect.right > self.rect.right:
				self.vlx = 2

		elif self.distance_x <= 0 and colision != True:
			self.vlx = 0
			if self.game.player.rect.top > self.rect.top:
				self.vly = 2
			elif  self.game.player.rect.bottom < self.rect.bottom:
				self.vly = -2
			
		if self.vlx > 0:		
			self.angle = -90
		elif self.vlx < 0:
			self.angle = 90
		if self.vly > 0:
			self.angle = 180
		elif self.vly < 0:
			self.angle = 0

		self.image = pg.transform.rotate(self.image_e,self.angle)
		self.image = pg.transform.scale(self.image,(40,40))

	def shot(self):

		if self.rect.y == self.game.player.rect.y or self.rect.x == self.game.player.rect.x:
			self.cont_shot +=1

			if self.cont_shot >= 30:	
				self.cannon(True)
				self.cont_shot = 0
		else:
			self.cont_shot = 0

class Tank(Sprite):

	def __init__(self,x,y,game,value = 0):
		self.value = value
		self.image_a = image["tank_{}".format(value)]
		self.image = self.image_a
		self.image = pg.transform.scale(self.image,(40,40))
		self.mask = pg.mask.from_surface(self.image)

		Sprite.__init__(self,x,y,game)
	
		self.joystick =  pg.joystick.Joystick(value)  if pg.joystick.get_count() > 0 else None
		self.joystick.init() if self.joystick != None else None
	
		self.angle = 0
		self.move_bool = 0
		self.direction = (0,0)


		self.vidas = 3

	def update(self):

		self.move()
		self.collided()


		for shot in self.game.bullets:
			if shot.rect.colliderect(self.rect):
				if shot.value != self.value:
					self.vidas -=1
					self.game.bullets.remove(shot)
					#self.kill()


	def rotate(self,xbool):

		if xbool == 1:
			self.angle += 90
			if self.angle >= 360:
				self.angle = 0
		else:
			self.angle -= 90
			if self.angle <= -360:
					self.angle = 0
		
		self.image = pg.transform.rotate(self.image_a,self.angle)
		self.image = pg.transform.scale(self.image,(40,40))

	def move(self):
		
		radians = math.radians(self.angle)

		if self.move_bool == 1:
			self.vlx = 4 * - math.sin(radians)
			self.vly = 4 * - math.cos(radians)

		else:
			self.vlx = 0
			self.vly = 0

class Hexagons(pg.sprite.Sprite):

	def __init__(self,x,y,surface,game):
		
		pg.sprite.Sprite.__init__(self)
		
		r = 40
		self.image = pg.Surface((r*2 + 3, r*2 + 2))
		self.image.set_colorkey((0,0,0))
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.pointlist = [ (  r + r*math.cos( math.radians(60*i)), r + r*math.sin( math.radians(60*i))) for i in range(6) ]
		self.rect = pg.Rect((x,y),(self.width,self.height))
		pg.draw.polygon(self.image,pg.Color("#838383"),self.pointlist,4)
		surface.blit(self.image,(x,y))
		self.game = game

	def no_collided(self):
		pass
					#if hexagon.rect.colliderect(self.player.rect):	
			#	if self.player.rect.x <=  hexagon.x + hexagon.pointlist[0][0] \
			#		and self.player.rect.x >= hexagon.x + hexagon.pointlist[1][0] \
			#		and self.player.rect.y <= hexagon.y + hexagon.pointlist[0][1]:
			#			self.player.rect.y = self.player.rect.right - hexagon.pointlist[0][0]

class Rect(pg.sprite.Sprite):

	def __init__(self,x,y,game,surface):
		pg.sprite.Sprite.__init__(self)
		width = 42
		height = 42
		self.game = game
		self.image = image["Rect"]
		self.image =  self.image.subsurface((0,42),(width,height))
		self.rect = self.image.get_rect() 
		self.rect.x = x
		self.rect.y = y 
		self.rect.x,y= x,y
		surface.blit(self.image,self.rect)

class Tiled:

	def __init__(self,lvl,game):
		self.lvl = lvl
		self.list_polygon = []
		self.game = game
			
	def make_map(self,SPACEMAP):
		tmp_surface = pg.Surface(self.game.surface.get_size())
		tmp_surface.fill(pg.Color("#06095A"))

		for i,lista in enumerate(self.lvl):
			for j,tile in enumerate(lista):

				if tile == "0":
					pass
				elif tile == "1":
					self.game.obs.add(Rect(j*SPACEMAP,i *SPACEMAP,self.game,tmp_surface))
				elif tile == "2":
					self.game.objs.add(Box(j*SPACEMAP,i *SPACEMAP,self.game))
				elif tile == "3":
					self.game.enemies.add(Enemy(j*SPACEMAP,i *SPACEMAP,self.game))
				elif tile == "4":
					self.game.player = Tank(j*SPACEMAP,i *SPACEMAP,self.game)
					self.game.sprites.add(self.game.player)
				elif tile == "5":
					self.game.obs.add(Hexagons(j*SPACEMAP,i*SPACEMAP,tmp_surface,self.game))
					
		return tmp_surface

class Game:

	def __init__(self,SURFACE,lvl_map):

		self.player = None
		self.load()

		#Map
		self.lvl_map = lvl_map
		SPACEMAP = 42

		#Temp
		self.lvl = "lvl_0"
		self.tile = Tiled(self.lvl_map[self.lvl],self)
		self.mission = Mission(self)

		#Surface
		self.surface = SURFACE
		self.WIDTH = self.surface.get_width()
		self.HEIGHT =  self.surface.get_height()

		self.tile_image = self.tile.make_map(SPACEMAP)


	def load(self):
		#__GROUP__#
		
		self.bullets = pg.sprite.Group()
		self.enemies = pg.sprite.Group()
		self.sprites = pg.sprite.Group()
		self.obs = pg.sprite.Group()
		self.objs = pg.sprite.Group()
		self.effect = pg.sprite.Group()

	def update(self):

		self.enemies.update()
		self.sprites.update()
		self.objs.update()
		self.bullets.update()
		self.mission.update()
		self.effect.update()


	def draw(self):
		
		self.surface.blit(self.tile_image,(0,0))
		self.bullets.draw(self.surface)
		self.objs.draw(self.surface)
		self.sprites.draw(self.surface)
		self.enemies.draw(self.surface)
		self.effect.draw(self.surface)

def loop():

	WIDTH = len(lvl_0[0])*SPACEMAP
	HEIGHT = len(lvl_0)*SPACEMAP

	SCREEN = pg.display.set_mode((WIDTH,HEIGHT))		
	pg.display.set_caption(" Lemon Tank ")


	exit = False
	clock = pg.time.Clock()
	game = Game(SCREEN,lvl_map)
	
	while exit != True:
		clock.tick(60)
		for event in pg.event.get():
			if event.type == pg.QUIT:
				exit = True

			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					exit = True
				if event.key == pg.K_SPACE:
					game.player.cannon(True)
				elif event.key == pg.K_LEFT:
					game.player.rotate(1)
				elif event.key == pg.K_RIGHT:
					game.player.rotate(-1)
				elif event.key == pg.K_UP:
					game.player.move_bool = 1

			elif event.type == pg.JOYBUTTONUP:
				if event.button == 3:
					game.player.cannon(True)

			if event.type == pg.JOYHATMOTION:
				
				game.player.rotate(event.value[0] * -1) if event.value[0] != 0 else 0 
				game.player.move_bool = 1 if event.value[1] == 1 else 0
			if event.type == pg.KEYUP:
				if event.key == pg.K_UP:
					game.player.move_bool = 0

		
		game.update()
		game.draw()
		


		pg.display.flip()

if __name__ == "__main__":
	loop()
	pg.quit()
