import pytmx
import pygame as pg
import math

from src.sprites import Brick, Player


class Collision:
    bricks = pg.sprite.Group()


    @classmethod
    def load(cls,lvl_map_tmx:str):
        for tile_object in pytmx.TiledMap(lvl_map_tmx).objects:
            if tile_object.name == 'player':
                pass
            elif tile_object.name == 'brick':
                block = Brick(tile_object.x,tile_object.y,tile_object.width,tile_object.height)
                cls.bricks.add(block)


    @classmethod
    def collide_with_objects(cls,player: dict):
        body = pg.Rect(player["x"], player["y"], Player.SIZE_BODY_RECT[0],Player.SIZE_BODY_RECT[1])

        for brock in cls.bricks:
            width_rect = body.w * body.w
            height_rect = body.h * body.h

            radius_player = math.sqrt( width_rect  + height_rect ) / 2.0

            width_block = brock.rect.w * brock.rect.w
            height_block = brock.rect.h * brock.rect.h

            radius_block = math.sqrt(width_block + height_block) / 2.0
            radius_sum = radius_block + radius_player

            dx =  brock.rect.right / 2 -( body.right / 2)
            dy =  brock.rect.bottom / 2 - (body.bottom / 2)

            distance = math.sqrt(dx* dx  + dy*dy )
            separation = radius_sum - distance

            if body.colliderect(brock.rect):
                if distance >= radius_sum:
                    pass

                if distance != 0:
                    dx /= distance
                    dy /= distance
                    player["x"] -= dx * separation * 0.125
                    player["y"] -= dy  * separation * 0.125