#!/usr/bin/python3

import pygame as pg
#Package Game
from script.tiled_lvl import Tiled,SPACEMAP,lvl_map
from script.interface import Interface

#paquete script/sub paquete server
from server_tcp.network import Network

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
		self.sprites = pg.sprite.Group()
		self.obs = pg.sprite.Group()
		self.objs = pg.sprite.Group()
		self.enemies = pg.sprite.Group()


	def update(self):
		for player in self.sprites:
			player.update()
			self.collided(player)	
	
		self.collide_shot(self.player,self.player.bullets,self.player_2.bullets)	
		self.objs.update()


	def draw(self):
		self.surface.blit(self.tile_image,(0,0))
		self.objs.draw(self.surface)
		self.player.draw(self.surface)
		self.player_2.draw(self.surface)


	def collided(self,player):
		"""Uso las cajas como barrera, así que esto no es necesario"""

		# if player.rect.right >= self.WIDTH: player.rect.right = self.WIDTH
		# elif player.rect.left <= 0: player.rect.left = 0

		# if player.rect.bottom >= self.HEIGHT: player.rect.bottom = self.HEIGHT
		# elif player.rect.top <= 0: player.rect.top = 0

		player.rect.centerx += player.vlx

		player.collided_group((1,0),self.sprites)
		player.collided_group((1,0),self.obs)
		player.collided_group((1,0),self.enemies)

		player.rect.centery += player.vly

		player.collided_group((0,1),self.sprites)
		player.collided_group((0,1),self.obs)
		player.collided_group((0,1),self.enemies)


	def collide_shot(self,player,group_a,group_b):
		self.limite_disparo(group_a)
		self.limite_disparo(group_b)

		if pg.sprite.groupcollide(group_a,group_b,1,1):
			pass

		for shot in group_b:
			if pg.sprite.collide_mask(self.player,shot):		
				self.player.lifes_all -=1
				shot.kill()

		for shot in group_a:
			if pg.sprite.collide_mask(self.player_2,shot):
				self.player_2.lifes_all -=1
				shot.kill()

	def limite_disparo(self,group):
		for bullet in group:
			if  (0 > bullet.rect.x or bullet.rect.x > self.WIDTH 
				or  0 > bullet.rect.y or bullet.rect.y > self.HEIGHT): 
				bullet.kill()

			if (pg.sprite.spritecollide(bullet,self.obs,0) 
			or pg.sprite.spritecollide(bullet,self.objs,0)): 
				bullet.explosion()

			for box in self.objs:
				if box.rect.colliderect(bullet.rect):
					bullet.explosion()
					box.kill()


def loop():

	# -----------Iniciando  Cliente
	HOST = input('ENTER IP OF THE SERVER: ')
	PORT = input('ENTER PORT IP OF THE SERVER: ')
    
	print("\n")

	n = Network(HOST,PORT)


	map_tmp = lvl_map['lvl_0']

	# -----calculando el ancho y alto de la superficie 

	WIDTH = len(map_tmp[0])*SPACEMAP
	HEIGHT = len(map_tmp)*SPACEMAP

	SCREEN = pg.display.set_mode((WIDTH,HEIGHT + 42))		
	SURFACE = pg.Surface((WIDTH,HEIGHT))


	exit = False
	clock = pg.time.Clock()
	game = Game(SURFACE,lvl_map)
	
	#-----------

	start_key = n.get_key()

	game.player.data = start_key

	game.player.rect.x = start_key['x']
	game.player.rect.y = start_key['y']
	
	game.player.value = start_key['player'] 
	game.player.value_player() 

	p2key = n.send(game.player.data)
	game.player_2.value = p2key['player'] 	
	game.player_2.value_player() 


	interface = Interface(game)
	pg.display.set_caption(f" Lemon Tank - PLAYER {start_key['player'] + 1} ")


	while exit != True:
		
		clock.tick(60)
		for event in pg.event.get():
			if event.type == pg.QUIT:
				exit = True


			if event.type == pg.KEYDOWN:

				if event.key == pg.K_ESCAPE: 
					exit = True
				
				if event.key == pg.K_SPACE:
					game.player.data['SPACE'] = True
					
				if event.key == pg.K_LEFT: 
					game.player.data['LEFT'] = True
					game.player.rotate(1)

				if event.key == pg.K_RIGHT: 
					game.player.data['RIGHT'] = True
					game.player.rotate(-1)
				
				if event.key == pg.K_UP: 
					game.player.data['UP'] = True					
					game.player.move_bool = 1

			if event.type == pg.KEYUP:				

				 if event.key == pg.K_SPACE:
				 	game.player.data['SPACE'] = False
				 
				 if event.key == pg.K_RIGHT:
				 	game.player.data['RIGHT'] = False
				 
				 if event.key == pg.K_LEFT:
				 	game.player.data['LEFT'] = False

				 if event.key == pg.K_UP:
					 game.player.data['UP'] = False
					 game.player.move_bool = 0


		#-------------- Recibir los datos del jugador 2 y luego asignación correspondiente

		p2key = n.send(game.player.data)

		game.player_2.rect.x = p2key['x']
		game.player_2.rect.y = p2key['y']


		if game.player.data['SPACE'] == True:

			if game.player.load == True: 
				game.player.fire = True


		#Esto no funciona muy bien, estoy pensando enviar los 2 dict de los jugadores en vez de 1 del jugador contrario
		
		if p2key['SPACE'] == True:
			if p2key['fire_load'] == True:
			#if game.player_2.cannon.load == True: 
				game.player_2.fire = True

		if p2key['angle'] != game.player_2.angle:
			if p2key['RIGHT'] == True:
				game.player_2.rotate(-1)

			elif p2key['LEFT'] == True:
				game.player_2.rotate(1)
	
		#actualizar angulo antes de mover 
		game.player_2.angle = p2key['angle']
		#con esto llevo la cuenta de las vidas actuales
		game.player_2.lifes_all = p2key['lifes']

		if p2key['UP']:
			game.player_2.animation()
			game.player_2.rotate_img()


		game.update()
		game.draw()	

		SCREEN.blit(SURFACE,(0,0))
		interface.update(SCREEN)

		pg.display.flip()

if __name__ == "__main__":
	loop()
	pg.quit()
