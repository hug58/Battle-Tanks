#!/usr/bin/python3

import pygame as pg
import pytmx

#Package Game
from script.tiled_lvl import TileMap
from script.interface import Interface
from script.camera import Camera
from script.player import Tank
from script.elements import Brick

#paquete script/sub paquete server
from server_tcp.network import Network

class Game:

	def __init__(self,SURFACE,lvl_map,screen_size):
		self.player = None
		self.player_2 = None
		

		#Map
		self.lvl_map = lvl_map
		#SPACEMAP = 42

		#Temp
		#self.lvl = 'lvl_1'
		
		self.tile = TileMap(self.lvl_map)
		self.tile_image = self.tile.make_map()
		self.tile_rect = self.tile_image.get_rect()
		

		#Surface
		self.surface = SURFACE
		#self.WIDTH = self.surface.get_width()
		#self.HEIGHT =  self.surface.get_height()


		#camera
		self.camera = Camera(self.tile.WIDTH,
							self.tile.HEIGHT,
							screen_size,
							)


		#--------------
		self.load()

	def load(self):
		self.sprites = pg.sprite.Group()
		self.obs = pg.sprite.Group()
		self.objs = pg.sprite.Group()

		for tile_object in self.tile.tmxdata.objects:
			
			if tile_object.name == 'brick':
					brick = Brick(tile_object.x,
								tile_object.y,
								tile_object.width,
								tile_object.height,)

					self.obs.add(brick)
					self.objs.add(brick)
			
			elif tile_object.name == 'Player_1': 
				self.player = Tank(tile_object.x,tile_object.y)
				self.sprites.add(self.player)

			elif tile_object.name == 'Player_2':
				self.player_2 = Tank(tile_object.x,tile_object.y,value=1)
				self.sprites.add(self.player_2)



	def update(self):

		self.camera.update(self.player)

		for player in self.sprites:
			player.update()
			self.collided(player)	
	
		self.collide_shot(self.player,self.player.bullets,self.player_2.bullets)	
		self.objs.update()

	def draw_bullet(self,player):
		for bullet2 in player.bullets:
			self.surface.blit(bullet2.image,self.camera.apply(bullet2))


	def draw(self):
		self.surface.blit(self.tile_image,self.camera.apply_rect(self.tile_rect))
		
		#for objs in self.objs:
		#	self.surface.blit(objs.image,self.camera.apply(objs))

		for player in self.sprites:		
			self.draw_bullet(player)
			self.surface.blit(player.image,self.camera.apply(player))


	def collided(self,player):

		############

		if player.rect.right >= self.tile.WIDTH: player.rect.right = self.tile.WIDTH
		elif player.rect.left <= 0: player.rect.left = 0


		if player.rect.bottom >= self.tile.HEIGHT: player.rect.bottom = self.tile.HEIGHT
		elif player.rect.top <= 0: player.rect.top = 0

		############

		player.rect.centerx += player.vlx

		player.collided_group((1,0),self.sprites)
		player.collided_group((1,0),self.obs)

		player.rect.centery += player.vly

		player.collided_group((0,1),self.sprites)
		player.collided_group((0,1),self.obs)

		############

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
			if  (0 > bullet.rect.x or bullet.rect.x > self.tile.WIDTH 
				or  0 > bullet.rect.y or bullet.rect.y > self.tile.HEIGHT): 
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
	#PORT = input('ENTER PORT IP OF THE SERVER: ')
	PORT = 10030

	print('\n')
	n = Network(HOST,PORT)


	map_tmp = 'maps/map_0.tmx' #lvl_map['lvl_0']
	# -----calculando el ancho y alto de la superficie 

	WIDTH =  800 #len(map_tmp[0])*SPACEMAP
	HEIGHT = 400 #len(map_tmp)*SPACEMAP

	 

	#---- + 42 para la interface de abajo
	SCREEN = pg.display.set_mode((WIDTH,HEIGHT + 42))		
	SURFACE = pg.Surface((WIDTH,HEIGHT))


	exit = False
	clock = pg.time.Clock()
	game = Game(SURFACE,
				map_tmp,
				(WIDTH,HEIGHT))
	
	#-----------

	start_key = n.get_key()

	game.player.data = start_key	
	game.player.value = start_key['player'] 
	game.player.dict_socket(start_key)
	game.player.value_player() 


	p2key = n.send(game.player.data)
	game.player_2.value = p2key['player'] 	
	game.player.dict_socket(p2key)
	game.player_2.value_player() 

	SIZE = (WIDTH,HEIGHT)
	interface = Interface(game,SIZE)
	pg.display.set_caption(' Lemon Tank - PLAYER {value} '
						.format(value = start_key['player'] + 1))
	
	#pg.display.set_caption(f' Lemon Tank - PLAYER {start_key['player'] + 1} ')


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
				print("FIRE!")
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

if __name__ == '__main__':
	loop()
	pg.quit()
