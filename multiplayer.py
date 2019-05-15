
from server_tcp.network import Network

from script import *
from script.tiled_lvl import Tiled,SPACEMAP,lvl_map
from script.mission import Mission
from script.interface import Interface



"""Leer y crear cadenas de la posición del tank"""

client_number = 0


# def read_pos(str):
# 	string = str.split(",")
# 	return int(string[0]),int(string[1])       

# def make_pos(tup):
# 	return str(tup[0]) + "," + str(tup[1])

class Game:

	def __init__(self,SURFACE,lvl_map):

		self.player = None
		self.player_2 = None
		
		self.load()

		#Map
		self.lvl_map = lvl_map
		SPACEMAP = 42

		#Temp
		self.lvl = "lvl_1"
		
		self.tile = Tiled(self.lvl_map[self.lvl],self)

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
		#self.sprites.update()
		self.objs.update()
		self.bullets.update()
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

	map_tmp = lvl_map['lvl_0']

	# -----calculando el ancho y alto de la superficie 

	WIDTH = len(map_tmp[0])*SPACEMAP
	HEIGHT = len(map_tmp)*SPACEMAP

	SCREEN = pg.display.set_mode((WIDTH,HEIGHT + 42))		
	SURFACE = pg.Surface((WIDTH,HEIGHT))

	pg.display.set_caption(" Lemon Tank ")

	exit = False
	clock = pg.time.Clock()
	game = Game(SURFACE,lvl_map)
	interface = Interface(game)
	
	# -----------Iniciando  Cliente

	n = Network()
	start_key = n.get_key()

	game.player.teclas = start_key

	game.player.rect.x = start_key['x']
	game.player.rect.y = start_key['y']


	while exit != True:
		
		clock.tick(60)
		for event in pg.event.get():
			if event.type == pg.QUIT:
				exit = True

			if event.type == pg.KEYDOWN:

				print(event.key)
				

				if event.key == pg.K_ESCAPE: 
					exit = True
				
				if event.key == pg.K_SPACE:
					game.player.teclas['SPACE'] = True
					
					if game.player.cannon.load == True: 
						game.player.cannon.fire = True
				
				if event.key == pg.K_LEFT: 
					game.player.teclas['LEFT'] = True
					
					game.player.rotate(1)

				if event.key == pg.K_RIGHT: 
					game.player.teclas['RIGHT'] = True
					game.player.rotate(-1)
				
				if event.key == pg.K_UP: 
					game.player.teclas['UP'] = True					
					game.player.move_bool = 1

			if event.type == pg.KEYUP:				

				 if event.key == pg.K_SPACE:
				 	game.player.teclas['SPACE'] = False
				 
				 if event.key == pg.K_RIGHT:
				 	game.player.teclas['RIGHT'] = False
				 
				 if event.key == pg.K_LEFT:
				 	game.player.teclas['LEFT'] = False

				 if event.key == pg.K_UP:
				 	game.player.teclas['UP'] = False


			# elif event.type == pg.JOYBUTTONUP:
			# 	if event.button == 3: game.player.cannon.fire = True

			# if event.type == pg.JOYHATMOTION:
			# 	game.player.rotate(event.value[0] * -1) if event.value[0] != 0 else 0 
			# 	game.player.move_bool = 1 if event.value[1] == 1 else 0
			
			if event.type == pg.KEYUP:
				if event.key == pg.K_UP:
					game.player.move_bool = 0

		


		#-------------- Recibir los datos del jugador 2 y luego asignación correspondiente

		#p2pos = n.send(make_pos((game.player.rect.x,game.player.rect.y)))
		#p2pos = read_pos(p2pos)

		#game.player_2.rect.x = p2pos[0]
		#game.player_2.rect.y = p2pos[1]

		p2key = n.send(game.player.teclas)
		#game.player_2.teclas = p2key

		game.player_2.rect.x = p2key['x']
		game.player_2.rect.y = p2key['y']


		if p2key['SPACE'] == True:
			if game.player_2.cannon.load == True: 
				game.player_2.cannon.fire = True

		if p2key['angle'] != game.player_2.angle:
			if p2key['RIGHT'] == True:
				game.player_2.rotate(-1)

			elif p2key['LEFT'] == True:
				game.player_2.rotate(1)

		if p2key['UP']:
			game.player_2.animation()
			game.player_2.rotate_img()

		game.player_2.angle = p2key['angle']


		game.player.update()
		game.player_2.update()


		game.update()		
		SCREEN.blit(SURFACE,(0,0))
		interface.update()
		interface.draw(SCREEN)

		pg.display.flip()

if __name__ == "__main__":
	loop()
	pg.quit()
