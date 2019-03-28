import game
import pygame as pg

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
					self.game.obs.add(game.Rect(j*SPACEMAP,i *SPACEMAP,self.game,tmp_surface))
				elif tile == "2":
					self.game.objs.add(game.Box(j*SPACEMAP,i *SPACEMAP,self.game))

				elif tile == "3":
					#Primer jugador
					self.game.sprites.add(game.Tank(j*SPACEMAP,i *SPACEMAP,self.game))
				elif tile == "4":
					#Segundo Jugador
					self.game.sprites.add(game.Tank(j*SPACEMAP,i *SPACEMAP,self.game,1))
				elif tile == "5":
					self.game.obs.add(game.Hexagons(j*SPACEMAP,i*SPACEMAP,tmp_surface,self.game))
					
		return tmp_surface


class Load_game:

	def __init__(self,SURFACE,lvl_map):

		self.load()

		#Map
		self.lvl_map = lvl_map
		SPACEMAP = 42

		#Temp
		self.lvl = "lvl_0"
		self.tile = Tiled(self.lvl_map[self.lvl],self)

		#Surface
		self.surface = SURFACE
		self.WIDTH = self.surface.get_width()
		self.HEIGHT =  self.surface.get_height()

		self.tile_image = self.tile.make_map(SPACEMAP)

		#Red
		#self.server = Server()


	def load(self):
		#__GROUP__#
		
		self.bullets = pg.sprite.Group()

		self.sprites = pg.sprite.Group()
		self.obs = pg.sprite.Group()
		self.objs = pg.sprite.Group()
		self.effect = pg.sprite.Group()

	def update(self):

		self.sprites.update()
		self.objs.update()
		
		self.bullets.update()
		self.effect.update()


	def draw(self):
		
		self.surface.blit(self.tile_image,(0,0))
		self.bullets.draw(self.surface)
		self.objs.draw(self.surface)
		self.sprites.draw(self.surface)
		self.effect.draw(self.surface)
		#self.send(SURFACE)

	#def send(self,surface):
		#self.server.send(surface)

def loop():

	#__CONSTANS__#

	SPACEMAP = 42

	lvl_0 = [

				"11111111111111111111111",
				"10000000000000000000001",
				"10000000000000000000001",			
				"10000000000000000000001",
				"10011000111110000110001",
				"10011000102011000110001",
				"10000000000000000000001",
				"10000000000000000000001",
				"10000000000000000000001",
				"10400000000000000300001",
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


	exit = False
	clock = pg.time.Clock()
	game = Load_game(SCREEN,lvl_map)
	
	while exit != True:
		clock.tick(60)

		for event in pg.event.get():
			if event.type == pg.QUIT:
				exit = True

			for sprites in game.sprites:

				if event.type == pg.KEYDOWN:
					if event.key == pg.K_ESCAPE:
						exit = True

					if sprites.value == 0:

						if event.key == pg.K_t:
							sprites.cannon(True)
						elif event.key == pg.K_a:
							sprites.rotate(1)
						elif event.key == pg.K_d:
							sprites.rotate(-1)
						elif event.key == pg.K_w:
							sprites.move_bool = 1


					if sprites.value == 1:
						
						if event.key == pg.K_p:
							sprites.cannon(True)
						elif event.key == pg.K_j:
							sprites.rotate(1)
						elif event.key == pg.K_l:
							sprites.rotate(-1)
						elif event.key == pg.K_i:
							sprites.move_bool = 1
							

				if event.type == pg.KEYUP:
					if sprites.value == 0:
						if event.key == pg.K_w:
							sprites.move_bool = 0

					if sprites.value == 1:
						if event.key == pg.K_i:
							sprites.move_bool = 0


			# elif event.type == pg.JOYBUTTONUP:
			# 	if event.button == 3:
			# 		game.player.cannon(True)

			# if event.type == pg.JOYHATMOTION:
			# 	game.player.rotate(event.value[0] * -1) if event.value[0] != 0 else 0 
			# 	game.player.move_bool = 1 if event.value[1] == 1 else 0
				
		game.update()
		game.draw()

		pg.display.flip()

if __name__ == "__main__":
	loop()
	pg.quit()
