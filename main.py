import random,os,sys,math
import pygame as pg

pg.display.init()
pg.mixer.init()
pg.joystick.init()

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
			"10000000000000000300001",
			"10400000000000000000001",
			"10000000000000000000001",
			"11111111111111111111111",

		]

lvl_map = {
	"lvl_0":lvl_0,
}


WIDTH = len(lvl_0[0])*SPACEMAP
HEIGHT = len(lvl_0)*SPACEMAP

SCREEN = pg.display.set_mode((WIDTH,HEIGHT))		
pg.display.set_caption(" Lemon Tank ")

image = {	
			"tank_0":pg.image.load(resolve_route("image/limonero_tank.png")),
			"enemy":pg.image.load(resolve_route("image/uvadero_tank.png")),
			"ball_0":pg.image.load(resolve_route("image/ball_a.png")),
			"Rect":pg.image.load(resolve_route("image/Rect.png")),
			"Box":pg.image.load(resolve_route("image/box.png")),

}

sound = { 
			"show":pg.mixer.Sound(resolve_route("sound/show.wav")),	
			"box":pg.mixer.Sound(resolve_route("sound/box.wav")),
}

pg.display.set_icon(image["tank_0"])



class Mission:
	def __init__(self,game):
		self.game = game
		self.objetivos = {

			"lvl_0": self.All_kill,
		}
		self.mission_actual = self.objetivos[self.game.lvl]


	def update(self):

		self.mission_actual()
		if self.mission_actual() == True:
			print("¡Mission COMPLET!")


	def All_kill(self):
		if len(self.game.sprites) > 1:
			return False
		else:
			return True

class Animation:
	
	def __init__(self,frames):
		self.current_frames = 0
		self.limit = len(frames)
		self.step = 15
		self.cont = 0
	def update(self):
		
		if self.cont == self.step:			
			if self.current_frames < self.limit:
				self.current_frames +=1
			
			if self.current_frames == self.limit:
				self.current_frames = 0
				
			self.cont = 0

		elif self.cont == 0:
			self.current_frames = 0

		self.cont +=1

class Box(pg.sprite.Sprite):
	def __init__(self,x,y,game):

		pg.sprite.Sprite.__init__(self)
		self.game = game
		self.box_img = image["Box"]
		self.image = self.box_img.subsurface((10,0),(10,10))
		self.image = pg.transform.scale(self.image,(30,30))
		self.rect = pg.Rect((x,y),self.image.get_size())
		
		self.frames = {
			0:(0,0),
			1:(10,0),
		}

		self.animation = Animation(self.frames)

	def update(self):

		frame = self.animation.current_frames
		self.animation.update()
		self.image = self.box_img.subsurface(self.frames[frame],(10,10))
		self.image = pg.transform.scale(self.image,(30,30))

class Bala(pg.sprite.Sprite):

	def __init__(self,point,angle,value,game):
		
		pg.sprite.Sprite.__init__(self)
		self.image_b = image["ball_{}".format(value)]
		self.image = pg.transform.rotate(self.image_b,angle)
		self.rect = self.image.get_rect()
		self.game = game
		radians = math.radians(angle)
		self.rect.x = (point[0][0] + (2 * math.sin(radians))) - self.rect.width//2 
		self.rect.y = point[0][1] + (2 * math.cos(radians)) - self.rect.height //2
		
		self.vlx = -10 * math.sin(radians)
		self.vly = -10 * math.cos(radians)

	def update(self):

		if  0 > self.rect.x or self.rect.x > WIDTH or  0 > self.rect.y or self.rect.y > HEIGHT:
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

	def cannon(self,fire):
		self.point_ball = ((self.rect.centerx,self.rect.centery),self.image.get_size())

		if fire == True:
			sound["show"].stop()
			sound["show"].play()
			self.game.balls.add(Bala(self.point_ball,self.angle,self.value,self.game))

	def collided(self):
	
		"""
		
			#colision_enemies = pg.sprite.collide_mask(self.game.player,self)
			#if colision_enemies != None:
			#	print("colisionamos!")
			#colision = pg.sprite.spritecollide(self,self.game.obs,0)

			#for block in colision:
			#	if self.rect.x < block.rect.x:
			#		self.rect.right = block.rect.x 
			#	if self.rect.x +  self.rect.width > block.rect.x + block.rect.width:
			#		self.rect.x = block.rect.x + block.rect.width
				#if self.vlx > 0:
				#	self.rect.right =   min(block.rect.left,self.rect.right)  
				#self.rect.right =   max(block.rect.left,self.rect.right)  
				#self.rect.top = max(block.rect.bottom,self.rect.top)


				#self.rect.left = max(self.rect.left,-(block.rect.right))

				#print(self.rect.x)
				#if self.vlx > 0:
				#	self.rect.right = block.rect.left
				#elif self.vlx < 0:
				#	self.rect.left = block.rect.right

			 #colision = pg.sprite.spritecollide(self,self.game.obs,0)

			#for block in colision:
			#	if self.vly > 0:
			#		self.rect.top = block.rect.bottom
			#	elif self.vly < 0:
			#		self.rect.bottom = block.rect.top
	
		"""

		if self.rect.right >= WIDTH:
			self.rect.right = WIDTH
		elif self.rect.left <= 0:
			self.rect.left = 0

		if self.rect.bottom >= HEIGHT:
			self.rect.bottom = HEIGHT
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
		self.image = pg.transform.flip(image["enemy"],0,1)
		self.image = pg.transform.scale(self.image,(40,40))
		Sprite.__init__(self,x,y,game)		
		#self.rect_camp = pg.Rect((self.rect.centerx,self.rect.centery),(50,50))
		self.direcciony = 1


		#self.vl = 1

	def update(self):
		self.kill() if pg.sprite.spritecollide(self,self.game.balls,1) else 0
		self.move()

		self.collided()
		#self.rect.x +=self.vlx
		#self.rect.y += self.vly	

	def move(self):
		

		for block in pg.sprite.spritecollide(self,self.game.obs,0):
			if block.rect.bottom > self.rect.top and block.rect.bottom < self.rect.bottom:
				print("ok")


		colision = rect_group(self.rect ,self.game.obs)
		
		self.distance_x = math.sqrt((self.rect.centerx - self.game.player.rect.centerx)**2)
		self.distance_y = math.sqrt((self.rect.centery - self.game.player.rect.centery)**2)

		if self.distance_x > 0 and colision != True:

			self.vly = 0


			if self.game.player.rect.left < self.rect.left:
				self.vlx = -2
			elif self.game.player.rect.right > self.rect.right:
				self.vlx = 2

		elif self.distance_x <= 0 or colision == 1:

			self.vlx = 0
			
			if self.game.player.rect.top > self.rect.top:
				self.vly = 2

			elif  self.game.player.rect.bottom < self.rect.bottom:
				self.vly = -2

			


		#colision = pg.sprite.spritecollide(self,self.game.abs)

		#self.distanciax = math.sqrt((self.rect.centerx - self.game.player.rect.centerx)**2)
		#self.distanciay = math.sqrt((self.rect.centery - self.game.player.rect.centery)**2)
		
		#if self.distanciax < 200 and self.distanciay <= 100:
		
	#	if self.game.player.rect.left < self.rect.left:
	#		self.vlx = -self.vl
	#	elif self.game.player.rect.right > self.rect.right:
	#		self.vlx = self.vl
	#	if self.game.player.rect.top > self.rect.top:
	#		self.vly = self.vl
	#	elif self.game.player.rect.bottom < self.rect.bottom:
	#		self.vly = - self.vl

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

	def update(self):

		self.move()
		self.collided()
		if pg.sprite.spritecollide(self,self.game.objs,1):
			sound["box"].play()

		#self.rect.x += self.vlx
		#self.rect.y += self.vly
		#self.rect.move_ip((self.vlx,self.vly))
	
	"""	def move(self):
			move = pg.key.get_pressed()
			if move[pg.K_LEFT] or self.direction[0] == -1:
				self.angle += 90
				self.image = pg.transform.rotate(self.image_a,self.angle)
				#self.angle +=2
				if self.angle >= 360:
					self.angle = 0
			if move[pg.K_RIGHT] or self.direction[0] == 1:
				self.angle -=90
				self.image = pg.transform.rotate(self.image_a,self.angle)
				#self.angle -=2
				if self.angle <= -360:
					self.angle = 0
			#radians = math.radians(self.angle) 

			if move[pg.K_UP] or self.direction[1] == 1:
				pass
				#self.vlx =  4 *   -math.sin(radians)
				#self.vly =  4 *   -math.cos(radians) 

			#self.image = pg.transform.rotate(self.image_a,self.angle)
			#self.rect = pg.Rect((self.rect.x,self.rect.y),(self.image.get_size()))		
			self.point_ball = [self.rect.centerx,self.rect.centery]
			self.mask = pg.mask.from_surface(self.image)
		"""

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
		#self.rect = pg.Rect((self.rect.x,self.rect.y),self.image.get_size())

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
		#self.image.fill((0,0,0))
		self.image.set_colorkey((0,0,0))
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.pointlist = [ (  r + r*math.cos( math.radians(60*i)), r + r*math.sin( math.radians(60*i))) for i in range(6) ]
		self.rect = pg.Rect((x,y),(self.width,self.height))
		#self.pointlist = ((40,20),(45,0),(45,44),(0,40),(0,60))
		#print(self.pointlist)
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
		#self.image.set_colorkey((0,0,0))
		#self.rect = self.image.get_rect()
		self.rect = self.image.get_rect() #pg.Rect((x,y),(width,height))
		self.rect.x = x
		self.rect.y = y 
		#pg.draw.rect(self.image,pg.Color("#838383"),self.rect,4)
		#surface.blit(self.image,self.rect)
		
		#pg.draw.rect(surface,pg.Color("#838383"),self.rect,4)
		self.rect.x,y= x,y
		surface.blit(self.image,self.rect)

class Tiled:

	def __init__(self,lvl,game):
		self.lvl = lvl
		self.list_polygon = []
		self.game = game
			
	def make_map(self):
		tmp_surface = pg.Surface((WIDTH,HEIGHT))
		tmp_surface.fill(pg.Color("#E4E4DC"))

		for i,lista in enumerate(self.lvl):
			for j,tile in enumerate(lista):

				if tile == "0":
					pass

				elif tile == "1":
					self.game.obs.add(Rect(j*SPACEMAP,i *SPACEMAP,self.game,tmp_surface))
								
				elif tile == "2":
					self.game.objs.add(Box(j*SPACEMAP,i *SPACEMAP,self.game))

				elif tile == "3":
					self.game.sprites.add(Enemy(j*SPACEMAP,i *SPACEMAP,self.game))

				elif tile == "4":
					self.game.player = Tank(j*SPACEMAP,i *SPACEMAP,self.game)
					self.game.sprites.add(self.game.player)

				elif tile == "5":
					self.game.obs.add(Hexagons(j*SPACEMAP,i*SPACEMAP,tmp_surface,self.game))
					
		return tmp_surface

class Game:

	def __init__(self):

		self.player = None
		self.enemies = [ Enemy(280,200,self)]#,Enemy(300,80,self)]
		self.load()

		#Temp
		self.lvl = "lvl_0"
		self.tile = Tiled(lvl_map[self.lvl],self)
		self.mission = Mission(self)

		self.tile_image = self.tile.make_map()

	def load(self):
		#__GROUP__#
		self.balls = pg.sprite.Group()
		self.sprites = pg.sprite.Group()
		self.obs = pg.sprite.Group()
		self.objs = pg.sprite.Group()

	def update(self):

		self.sprites.update()
		#self.obs.update()
		self.objs.update()
		self.balls.update()
		self.mission.update()

	def draw(self):
		
		SCREEN.blit(self.tile_image,(0,0))
		self.balls.draw(SCREEN)
		#self.obs.draw(SCREEN)
		self.objs.draw(SCREEN)
		self.sprites.draw(SCREEN)

def loop():

	exit = False
	clock = pg.time.Clock()
	game = Game()
	
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

			

		game.draw()
		game.update()
		
		pg.display.flip()

if __name__ == "__main__":
	loop()
	pg.quit()
