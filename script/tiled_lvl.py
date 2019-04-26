
import pygame as pg

from script.elements import Rect,Box
from script.enemy import Enemy
from script.player import Tank

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

#__CONSTANS__#
SPACEMAP = 42

class Tiled:

	def __init__(self,lvl,game):
		self.lvl = lvl
		self.list_polygon = []
		self.game = game
			
	def make_map(self,SPACEMAP):
		tmp_surface = pg.Surface(self.game.surface.get_size())
		#tmp_surface.fill(pg.Color("#06095A"))
		tmp_surface.fill(pg.Color("#000000"))
		#tmp_surface.fill((0,0,0))

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