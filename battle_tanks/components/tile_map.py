
import pygame as pg
import pytmx 

from battle_tanks import ROUTE


class TileMap:
    """ Load tilemap with tmx"""
    def __init__(self,filename):
        tm = pytmx.load_pygame(ROUTE(f"assets/maps/{filename}"),pixelaplha = True)
        self.WIDTH = tm.width * tm.tilewidth
        self.HEIGHT = tm.height * tm.tileheight
        self.tmxdata = tm


    def render(self,surface):
        """ load tilemap with surface """
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer,pytmx.TiledTileLayer):
                for x,y,gid in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile,(x* self.tmxdata.tilewidth,y* self.tmxdata.tileheight))


    def make_map(self):
        """ create surface object"""
        temp_surface = pg.Surface((self.WIDTH,self.HEIGHT))
        self.render(temp_surface)
        return temp_surface



    