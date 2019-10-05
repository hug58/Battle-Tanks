
import pygame as pg
import pytmx 

from scripts import ROUTE


class TileMap:
	def __init__(self,filename):
		ruta = ROUTE(filename)
		tm = pytmx.load_pygame(ruta,pixelaplha = True)
		self.WIDTH = tm.width * tm.tilewidth
		self.HEIGHT = tm.height * tm.tileheight
		self.tmxdata = tm

	def render(self,surface):
		ti = self.tmxdata.get_tile_image_by_gid
		for layer in self.tmxdata.visible_layers:
			if isinstance(layer,pytmx.TiledTileLayer):
				for x,y,gid in layer:
					tile = ti(gid)
					if tile: surface.blit(tile,(x* self.tmxdata.tilewidth,y* self.tmxdata.tileheight))
						
	def make_map(self):

		temp_surface = pg.Surface((self.WIDTH,self.HEIGHT)) #pg.SRCALPHA añadir transparencia a una surface 
		'''
		otra forma de añadir transparencia a una surface con un color en especifico (Negro). Es mucho más eficiente. 
		Muy importante si quieres añadir otra capa de fondo detrás del tilemap
		'''
		#temp_surface.set_colorkey((0,0,0))	
		self.render(temp_surface)

		'''
		Agregar transparencia a una surface ya creada
		'''
		#temp_surface.convert_alpha()
		
		return temp_surface


if __name__ == '__main__':
    pass

    