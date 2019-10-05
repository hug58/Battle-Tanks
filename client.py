
from scripts.game import Game
import pygame as pg
import socket

def loop():
			
	#HOST = input('IP: ')

	host_name = socket.gethostname()
	HOST = socket.gethostbyname(host_name)

	PORT = 10030

	print('\n')

	map_tmp = 'ASSETS/maps/zone_0.tmx'

	WIDTH,HEIGHT = 480,480
	SCREEN = pg.display.set_mode((WIDTH,HEIGHT + 36))

	exit = False
	clock = pg.time.Clock()

	SURFACE = pg.Surface((WIDTH,HEIGHT))
	game = Game((HOST,PORT),map_tmp,SURFACE)
	

	while exit != True:
		
		clock.tick(60)

		for event in pg.event.get():
			if event.type == pg.QUIT:
				exit = True


		game.update()
		game.draw()	

		SCREEN.blit(SURFACE,(0,0))


		pg.display.flip()

if __name__ == '__main__':
	loop()
	pg.quit()
