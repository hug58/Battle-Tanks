"""

	Hecho por hug58


	Ideas: bombas, disparo tipo escopeta, y escudos
	tiled con vista oculta

"""


import random,os,sys,math,socket
import pygame as pg

pg.display.init()
pg.mixer.init()
pg.joystick.init()
pg.font.init()


#__CONSTANS__#
SPACEMAP = 42
lvl_0 = [
			"11111111111111111111111",
			"10022000003000022000001",
			"10022000222000022000001",			
			"10000000000222000000001",
			"10011022111111130110001",
			"10011000100001100110001",
			"10011000002200000022001",
			"10011000002200000022001",
			"12221100002200322222221",
			"10600000002200000040001",
			"10001100222222222222001",
			"12222000002200000000001",
			"11111111111111111111111",
		]
lvl_map = {
	"lvl_0":lvl_0,
}

resolve_route = lambda route_relative: os.path.join(os.path.abspath("."),route_relative)	
Render_text =  lambda text: pg.font.Font("Pixel Digivolve.otf",30).render(text,2,pg.Color("#1CA4F4"))

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
			"tank_0": pg.image.load(resolve_route("image/limonero_tank.png")),
			"tank_1": pg.image.load(resolve_route("image/uvadero_tank.png")),
			"bullet_1": pg.image.load(resolve_route("image/bullet_a.png")),
			"bullet_0": pg.image.load(resolve_route("image/bullet_lvl2.png")),
			"rect": pg.image.load(resolve_route("image/Rect.png")),
			"box": pg.image.load(resolve_route("image/box.png")),
			"wave_shot" : pg.image.load("image/effect_shot.png"),
			"explosion": pg.image.load("image/effect_explosion.png"),
}

sound = { 
			"shot": pg.mixer.Sound(resolve_route("sound/shot.wav")),	
			"box": pg.mixer.Sound(resolve_route("sound/box.wav")),
			"boomsnd": pg.mixer.Sound(resolve_route("sound/boomsnd.wav")),
}

pg.display.set_icon(image["tank_0"])

class Life:
	def __init__(self,x,y,value):
		self.image = image[f"tank_{value}"]
		self.image = self.image.subsurface((0,20),(20,20))
		self.x = x
		self.y = y 

class Tablero:
	def __init__(self,game):
		self.game = game
		self.image = pg.Surface((self.game.WIDTH,42))
		
		self.vidas_player_1 = [ Life(120 + 40*(i+1),10,0) for i in range(3)]
		self.vidas_player_2 = [Life(632 + 42*(i+1),10,1) for i in range(3)] if len(self.game.sprites) > 1 else [] 
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
					print(f"Jugador {sprites.value + 1 } Perdió!") if len(self.game.sprites) > 1 else print(f"GAME OVER")


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

		#self.image.fill(pg.Color("#04441C"))
		self.image.fill((0,0,0))

		player1 = Render_text("Player 1")
		surface.blit(player1,(0,0))
		if len(self.vidas_player_2) > 0:
			player2 = Render_text("Player 2")
			surface.blit(player2,(500,0))


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
			pass
			#print("¡Mission COMPLET!")

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
			if self.current_frames < self.limit: self.current_frames +=1
			if self.current_frames == self.limit:
				self.current_frames = 0 if condition == 1 else self.current_frames
				
			self.cont = 0
		elif self.cont == 0:
			self.current_frames = 0

		self.cont +=1

class Box(pg.sprite.Sprite):

	def __init__(self,x,y,game):

		pg.sprite.Sprite.__init__(self,game.objs)
		self.box_img = image["rect"]
		self.image = self.box_img.subsurface((0,0),(42,42))
		self.rect = pg.Rect((x,y),self.image.get_size())		
		self.game = game

	def update(self):

		for bala in self.game.bullets:
			if self.rect.colliderect(bala.rect):
				bala.explosion()
				self.kill() 			

class Effect(pg.sprite.Sprite):
	def __init__(self,pos,angle,frames,size,key = "wave_shot"):

		pg.sprite.Sprite.__init__(self)
		self.effect = image[key]
		self.size = size

		self.image = self.effect.subsurface((0,0),self.size)
		self.image = pg.transform.scale(self.image,(self.size[0]*2,self.size[1]*2))
		self.rect = self.image.get_rect()

		self.radians = math.radians(angle)		
		self.rect.x = (pos[0] - (20 * math.sin(self.radians))) - self.rect.width//2 
		self.rect.y = pos[1] - (20 * math.cos(self.radians)) - self.rect.height //2
		
		self.pos = pos
		self.frames = frames

		self.animation = Animation(self.frames)
		self.animation.step = 2
		self.pos = pos

	def update(self):

		frame = self.animation.current_frames
		self.animation.update(0)
		self.image = self.effect.subsurface(self.frames[frame],self.size)
		self.image = pg.transform.scale(self.image,(self.size[0]*2,self.size[1]*2))

		if self.animation.current_frames >= len(self.frames): self.kill()

		self.rect.x = self.pos[0] - (30 * math.sin(self.radians)) - self.rect.width//2 
		self.rect.y = self.pos[1] - (35 * math.cos(self.radians)) - self.rect.height //2

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
		
		if  0 > self.rect.x or self.rect.x > self.game.WIDTH or  0 > self.rect.y or self.rect.y > self.game.HEIGHT: self.kill() 


		#Eliminar balas que chocan entre si

		for bullet in self.game.bullets:
			if bullet.value  != self.value:
				if self.rect.colliderect(bullet.rect): 
					self.game.bullets.remove(bullet)
					self.kill()


		# collided Rect--bals
		#collided Box-balls#
		if pg.sprite.spritecollide(self,self.game.obs,0) or pg.sprite.spritecollide(self,self.game.objs,0): self.explosion()
			
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
		self.game.effect.add(Effect(self.point_ball,self.angle,frames, size = (14,14), key = "explosion"))
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
		
		if self.cont < 40: 
			self.cont +=1
			self.fire = False

		else: self.load = True

		if self.fire == True and self.cont >= 40 or automatico == True and self.cont >= 40:
			self.point_ball = ((self.sprite.rect.centerx,self.sprite.rect.centery))
			sound["shot"].stop()
			sound["shot"].play()
			self.game.effect.add(Effect(self.point_ball,self.sprite.angle,self.effect_frames,size = (16,15)))
			self.game.bullets.add(Bala(self.point_ball,self.sprite.angle,self.sprite.value,self.game))
			self.load = False
			self.cont = 0

class Sprite(pg.sprite.Sprite):
	
	def __init__(self,x,y,game):

		pg.sprite.Sprite.__init__(self)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.vlx = 0
		self.vly = 0
		
		self.angle = 0		
		self.game = game

		self.cannon = Cannon(self.game,self)

		self.frames = { 0:(0,0), 1:(0,20), 2:(0,40),}
		self.position = 0
		self.size = (20,20)

	def collided(self):
	
		if self.rect.right >= self.game.WIDTH: self.rect.right = self.game.WIDTH
		elif self.rect.left <= 0: self.rect.left = 0

		if self.rect.bottom >= self.game.HEIGHT: self.rect.bottom = self.game.HEIGHT
		elif self.rect.top <= 0: self.rect.top = 0

		self.rect.x += self.vlx
		colision = pg.sprite.spritecollide(self,self.game.obs,0)
		
		for block in colision:
			if self.vlx > 0: self.rect.right = block.rect.left
			elif self.vlx < 0: self.rect.left = block.rect.right

		self.rect.y +=self.vly
		colision = pg.sprite.spritecollide(self,self.game.obs,0)
		
		for block in colision:
			if self.vly >= 0:
				self.rect.bottom = block.rect.top
				self.vly = 0
			elif self.vly < 0: self.rect.top = block.rect.bottom

	def animation(self):
		
			self.image = self.image_a.subsurface(self.frames[self.position],self.size) 			
			self.image = pg.transform.scale(self.image,self.size_scale)
			self.position +=1		
			if self.position >= len(self.frames): self.position = 0						

class Enemy(Sprite):
	
	def __init__(self,x,y,game):
		self.image_a = image["tank_1"]
		self.size_scale = (30,30)
		self.image = pg.transform.scale(self.image_a.subsurface((0,0),(20,20)),self.size_scale)
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
		self.image = pg.transform.scale(self.image,self.size_scale)

class Tank(Sprite):

	def __init__(self,x,y,game,value = 0):
		self.value = value
		self.image_a = image["tank_{}".format(value)]
		self.size_scale = (30,30)
		self.image = pg.transform.scale(self.image_a.subsurface((0,0),(20,20)),self.size_scale)
		Sprite.__init__(self,x,y,game)

		if  pg.joystick.get_count() > 0 and  pg.joystick.get_count() < 2 and value == 0: self.joystick =  pg.joystick.Joystick(value)
		elif pg.joystick.get_count() > 1 and value == 1: self.joystick =  pg.joystick.Joystick(value)
		else: self.joystick =  None
	
		if self.joystick != None: self.joystick.init()
	
		self.angle = 0
		self.move_bool = 0
		self.direction = (0,0)
		self.vidas = 3

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


	def rotate(self,xbool):

		if xbool == 1:
			self.angle += 90
			if self.angle >= 360: self.angle = 0
		else:
			self.angle -= 90
			if self.angle <= -360: self.angle = 0
		
		self.image = self.image_a.subsurface(self.frames[0],self.size)
		self.image = pg.transform.rotate(self.image,self.angle)
		self.image = pg.transform.scale(self.image,self.size_scale)

	def move(self):
		
		radians = math.radians(self.angle)

		if self.move_bool == 1:
			self.vlx = 3 * - math.sin(radians)
			self.vly = 3 * - math.cos(radians)
			self.animation()
			self.image = pg.transform.rotate(self.image,self.angle)

		else:
			self.vlx = 0
			self.vly = 0

class Rect(pg.sprite.Sprite):

	def __init__(self,x,y,game,surface):
		pg.sprite.Sprite.__init__(self)
		width = 42
		height = 42
		self.game = game
		self.image = image["rect"]
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
		#tmp_surface.fill(pg.Color("#06095A"))
		tmp_surface.fill((0,0,0))

		for i,lista in enumerate(self.lvl):
			for j,tile in enumerate(lista):

				if tile == "0": pass
				elif tile == "1": self.game.obs.add(Rect(j*SPACEMAP,i *SPACEMAP,self.game,tmp_surface))
				elif tile == "2": self.game.obs.add(Box(j*SPACEMAP,i *SPACEMAP,self.game))
				elif tile == "3": self.game.enemies.add(Enemy(j*SPACEMAP,i *SPACEMAP,self.game))
				elif tile == "4": 
					self.game.player = Tank(j*SPACEMAP,i *SPACEMAP,self.game)
					self.game.sprites.add(self.game.player)
					
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
		self.sprites = pg.sprite.GroupSingle()
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

		self.draw()

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

	SCREEN = pg.display.set_mode((WIDTH,HEIGHT + 42))		
	SURFACE = pg.Surface((WIDTH,HEIGHT))

	pg.display.set_caption(" Lemon Tank ")


	exit = False
	clock = pg.time.Clock()
	game = Game(SURFACE,lvl_map)
	tablero = Tablero(game)
	
	
	while exit != True:
		clock.tick(60)
		for event in pg.event.get():
			if event.type == pg.QUIT:
				exit = True

			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE: exit = True
				if event.key == pg.K_SPACE:
					if game.player.cannon.load == True: game.player.cannon.fire = True
				elif event.key == pg.K_LEFT: game.player.rotate(1)
				elif event.key == pg.K_RIGHT: game.player.rotate(-1)
				elif event.key == pg.K_UP: game.player.move_bool = 1

			elif event.type == pg.JOYBUTTONUP:
				if event.button == 3: game.player.cannon.fire = True

			if event.type == pg.JOYHATMOTION:
				game.player.rotate(event.value[0] * -1) if event.value[0] != 0 else 0 
				game.player.move_bool = 1 if event.value[1] == 1 else 0
			if event.type == pg.KEYUP:
				if event.key == pg.K_UP:
					game.player.move_bool = 0

		
		game.update()		
		SCREEN.blit(SURFACE,(0,0))
		tablero.update()
		tablero.draw(SCREEN)

		pg.display.flip()

if __name__ == "__main__":
	loop()
	pg.quit()
