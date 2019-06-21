
import pygame as pg

from script import resolve_route
from script.elements import Rect,Box,Gun
from script.player import Tank

#----FILA == NUMERO DE ELEMENTOS[STRINGS] DEL ARRAY
#----COLUMNA == NUMERO DE CARACTERES DEL STRING DEL ELEMENTO

def quitar_ultimo_elemento(string):
	if string[-1] == '\n':
		return string[:-1]
	else:
		return string

relative_route = resolve_route('maps','.',)
#archivo_0 = open(f'{relative_route}/map_0.txt','r')
#archivo_1 = open(f'{relative_route}/map_1.txt','r')
archivo_0 = open('{}/map_0.txt'.format(relative_route),'r')
archivo_1 = open('{}/map_1.txt'.format(relative_route),'r')


map_0 = list(map(quitar_ultimo_elemento,archivo_0.readlines()))
map_1 = list(map(quitar_ultimo_elemento,archivo_1.readlines()))

archivo_0.close()
archivo_1.close()


lvl_map = {
	'lvl_0':map_0,
	'lvl_1':map_1,
}

#__CONSTANS__#
SPACEMAP = 42

class Tiled:

	def __init__(self,map_lvl,game):
		self.map_lvl = map_lvl
		#self.list_polygon = []
		self.game = game
			
	def make_map(self,SPACEMAP):
		tmp_surface = pg.Surface(self.game.surface.get_size())
		#tmp_surface.fill(pg.Color('#06095A'))
		tmp_surface.fill(pg.Color('#000000'))
		#tmp_surface.fill((0,0,0))


		#Devuelve una fila[string] y numero de la fila actual
		for i,lista in enumerate(self.map_lvl):
			#Devuelve una columna[Caracter] y numero de la columna actual[Posicion del elemento]		
			for j,tile in enumerate(lista):

				if tile == '0': pass
				elif tile == '1': 
					self.game.obs.add(Rect(j*SPACEMAP,i *SPACEMAP,self.game,tmp_surface))
				elif tile == '2': 
					box = Box(j*SPACEMAP,i *SPACEMAP)
					self.game.obs.add(box)
					self.game.objs.add(box)
					
				elif tile == '3': 
					self.game.enemies.add(Enemy(j*SPACEMAP,i *SPACEMAP))
				elif tile == '4': 
					self.game.player = Tank(j*SPACEMAP,i *SPACEMAP)
					self.game.sprites.add(self.game.player)
				elif tile == '6':
					self.game.player_2 = Tank(j*SPACEMAP,i *SPACEMAP,value=1)
					self.game.sprites.add(self.game.player_2)
				elif tile == '8': 
					self.game.objs.add(Gun(j*SPACEMAP,i *SPACEMAP,self.game))

		return tmp_surface


if __name__ == '__main__':
    pass