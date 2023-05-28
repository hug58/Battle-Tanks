
from scripts import ROUTE,Text
from scripts.game import Game
import pygame as pg
import socket

def loop():
	# host_name = socket.gethostname() 
	# HOST = socket.gethostbyname(host_name)
	HOST = input("IP SERVER:")
 
	PORT = 10030

	print('\n')
	map_tmp = 'ASSETS/maps/zone_0.tmx'

	WIDTH,HEIGHT = 800,600
	SCREEN = pg.display.set_mode((WIDTH,HEIGHT + 36))

	exit = False
	clock = pg.time.Clock()

	SURFACE = pg.Surface((WIDTH,HEIGHT))
	game = Game((HOST,PORT),map_tmp,SURFACE)
	text_damage = Text((WIDTH//2,HEIGHT +16 ),f'Damage: {game._damage()} %')

	while exit != True:
		#limit fps 60
		clock.tick(30)
		for event in pg.event.get():
			if event.type == pg.QUIT:
				exit = True

		game.update()
		SCREEN.fill((0,0,0))
		game.draw()	
		text_damage.update(f'Damage: {game._damage()} %')
		text_damage.draw(SCREEN)

		SCREEN.blit(SURFACE,(0,0))
		pg.display.flip()



if __name__ == '__main__':
	loop()
	pg.quit()
