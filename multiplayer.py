import game

import pygame as pg
import threading as th

pg.display.init()
pg.mixer.init()
pg.joystick.init()
pg.font.init()

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
				elif tile == "1": self.game.obs.add(game.Rect(j*SPACEMAP,i *SPACEMAP,self.game,tmp_surface))
				elif tile == "2": self.game.obs.add(game.Box(j*SPACEMAP,i *SPACEMAP,self.game))
				elif tile == "4": self.game.sprites.add(game.Tank(j*SPACEMAP,i *SPACEMAP,self.game,1)) #Segundo jugador
				elif tile == "6": self.game.sprites.add(game.Tank(j*SPACEMAP,i *SPACEMAP,self.game)) #Primer jugador

		return tmp_surface

class Load_game(th.Thread):

	def __init__(self,lvl_map):
		th.Thread.__init__(self)


		WIDTH = len(game.lvl_0[0])*game.SPACEMAP
		HEIGHT = len(game.lvl_0)*game.SPACEMAP

		self.SCREEN = pg.display.set_mode((WIDTH,HEIGHT + 42))		
		self.surface = pg.Surface((WIDTH,HEIGHT))
		pg.display.set_caption(" Lemon Tank ")

		self.load()

		#Map
		self.lvl_map = lvl_map
		SPACEMAP = 42

		#Temp
		self.lvl = "lvl_0"
		self.tile = Tiled(self.lvl_map[self.lvl],self)

		#Surface
		self.WIDTH = self.surface.get_width()
		self.HEIGHT =  self.surface.get_height() 
		self.tile_image = self.tile.make_map(SPACEMAP)

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
		self.draw()

	def draw(self):
		
		self.surface.blit(self.tile_image,(0,0))
		self.bullets.draw(self.surface)
		self.objs.draw(self.surface)
		self.sprites.draw(self.surface)
		self.effect.draw(self.surface)


	def run(self):


		exit = False
		clock = pg.time.Clock()
		#load_game = Load_game(SURFACE,game.lvl_map)
		tablero = game.Tablero(self)


		while exit != True:
			clock.tick(60)

			for event in pg.event.get():
				if event.type == pg.QUIT: exit = True

				for sprites in self.sprites:

					if event.type == pg.KEYDOWN:
						if event.key == pg.K_ESCAPE: exit = True
						
						if sprites.value == 0:
							if event.key == pg.K_t:
								if sprites.cannon.load == True: sprites.cannon.fire = True
							elif event.key == pg.K_a: sprites.rotate(1)
							elif event.key == pg.K_d: sprites.rotate(-1)
							elif event.key == pg.K_w: sprites.move_bool = 1

						if sprites.value == 1:		
							if event.key == pg.K_p:
								if sprites.cannon.load == True: sprites.cannon.fire = True
							elif event.key == pg.K_j: sprites.rotate(1)
							elif event.key == pg.K_l: sprites.rotate(-1)
							elif event.key == pg.K_i: sprites.move_bool = 1
								
					if event.type == pg.KEYUP:
						if sprites.value == 0:
							if event.key == pg.K_w: sprites.move_bool = 0
						if sprites.value == 1:
							if event.key == pg.K_i: sprites.move_bool = 0


					if sprites.joystick != None:

						if event.type == pg.JOYBUTTONUP:
							if event.button == 3: sprites.cannon.fire = True
						if event.type == pg.JOYHATMOTION:
							sprites.rotate(event.value[0] * -1) if event.value[0] != 0 else 0 
							sprites.move_bool = 1 if event.value[1] == 1 else 0
						if event.type == pg.KEYUP:
							if event.key == pg.K_UP:
								sprites.move_bool = 0


			self.update()
			self.SCREEN.blit(self.surface,(0,0))
			tablero.update()
			tablero.draw(self.SCREEN)
			
			pg.display.flip()

		pg.quit()

if __name__ == "__main__":
	Load_game(game.lvl_map).run()
	pg.quit()
