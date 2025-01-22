import pytmx
import pygame as pg
import math
import pathlib
import random

from typing import Tuple, List
from collections.abc import Callable
from battle_tanks.sprites import Brick, Player, Block


class Collision:
    bricks = pg.sprite.Group()
    players:List[dict] = []
    size_screen:tuple = (0,0)
    lvl_map:str = ""
    game_state:bytes = b""
    positions = []


    @staticmethod
    def calculate_bullet_position(player_data:dict, distance:int) -> Tuple[int,int]:
        """
        :param player_data: getting x,y and angle_cannon
        :param distance: range of bullet

        """
        radian_angle = math.radians(player_data["angle_cannon"])
        vlx = distance * - math.sin(radian_angle)
        vly = distance * - math.cos(radian_angle)

        x = player_data["x"] + math.sin(radian_angle) * -30
        y = player_data["y"] + math.cos(radian_angle) * -30

        x += vlx
        y += vly

        return x, y


    @classmethod
    def check_collision_bullet(cls, player_data: dict, collision_radius: int) -> dict:
        """
        :param player_data: getting x,y and angle_cannon
        :param collision_radius: radius of collision
        """
        bullet_start_pos = Collision.calculate_bullet_position(player_data, 0)  # Starting position
        bullet_end_pos = Collision.calculate_bullet_position(player_data, 100)  # End position

        steps = 10
        for step in range(steps + 1):
            t = step / steps
            bullet_pos = (
                bullet_start_pos[0] + t * (bullet_end_pos[0] - bullet_start_pos[0]),
                bullet_start_pos[1] + t * (bullet_end_pos[1] - bullet_start_pos[1])
            )

            for brick in cls.bricks:
                brick: Brick
                target_pos = brick.rect.center
                distance = math.sqrt((bullet_pos[0] - target_pos[0]) ** 2 +
                                     (bullet_pos[1] - target_pos[1]) ** 2)
                collided = distance <= collision_radius
                if collided:
                    if isinstance(brick, Brick):
                        list_game_state: List[bytes] = cls.game_state.split(brick.data)
                        cls.game_state = b"".join(map(bytes, list_game_state))
                        brick.remove(cls.bricks)
                        return {
                            "type":5,
                            "x": brick.rect.x,
                            "y": brick.rect.y,
                            "w": brick.rect.w,
                            "h": brick.rect.h,
                        }

        return {}


    @classmethod
    def check_collision_player(cls, player_data: dict, collision_radius: int) -> dict:
        """
        :param player_data: getting x,y and angle_cannon
        :param collision_radius: radius of collision
        """
        bullet_start_pos = Collision.calculate_bullet_position(player_data, 0)  # Starting position
        bullet_end_pos = Collision.calculate_bullet_position(player_data, 100)  # End position

        steps = 10
        for step in range(steps + 1):
            t = step / steps
            bullet_pos = (
                bullet_start_pos[0] + t * (bullet_end_pos[0] - bullet_start_pos[0]),
                bullet_start_pos[1] + t * (bullet_end_pos[1] - bullet_start_pos[1])
            )



            for other_player in cls.players:
                if other_player.get("name") == player_data.get("name"):
                    continue

                target_pos = (other_player["x"], other_player["y"])
                distance = math.sqrt((bullet_pos[0] - target_pos[0]) ** 2 +
                                     (bullet_pos[1] - target_pos[1]) ** 2)
                collided = distance <= collision_radius
                if collided:
                    other_player["damage_indicator"] += Player.DAMAGE

                    if other_player["damage_indicator"] >= Player.MAX_DAMAGE:
                        random_index = random.randint(0, len(cls.positions) - 1)
                        other_player["damage_indicator"] = 0

                        other_player["x"] = cls.positions[random_index][0]
                        other_player["y"] = cls.positions[random_index][1]

                    return {
                            "type":7,
                            "player": other_player,
                    }

        return {}

    @classmethod
    def load(cls,lvl_map_tmx:str, func_tile_pack: Callable):
        _tile_map = pytmx.TiledMap(lvl_map_tmx)
        cls.lvl_map = pathlib.Path(lvl_map_tmx).name
        cls.size_screen = (_tile_map.width * _tile_map.tilewidth,
                           _tile_map.height * _tile_map.tileheight)

        for tile_object in _tile_map.objects:
            if tile_object.name == "player":
                cls.positions.append((int(tile_object.x),int(tile_object.y)))
            elif tile_object.name == "brick":
                brick = Brick(tile_object.x,tile_object.y,tile_object.width,tile_object.height)
                data_tile = func_tile_pack({
                    "x": brick.rect.x,
                    "y": brick.rect.y,
                    "h": brick.rect.h,
                    "w": brick.rect.w,
                    "type": 5
                })
                brick.data = data_tile

                """
                ONLY ADDED BRICK IN GAMESTATE.
                """
                cls.game_state += data_tile
                cls.bricks.add(brick)


            elif tile_object.name == "block":
                block = Block(tile_object.x,tile_object.y,tile_object.width,tile_object.height)
                cls.bricks.add(block)


    @classmethod
    def add_player(cls, player:dict):
        cls.players.append(player)

    @classmethod
    def collide_with_objects(cls,player: dict):
        """
        COLLIDE WITH X AND Y SIZE
        """
        if player["x"] <= 0:
            player["x"] = 0
        elif player["x"] + Player.SIZE_BODY_RECT[0] >= cls.size_screen[0]:
            player["x"] = cls.size_screen[0] - Player.SIZE_BODY_RECT[0]

        if player["y"] <= 0:
            player["y"] = 0
        elif player["y"] + Player.SIZE_BODY_RECT[1] >= cls.size_screen[1]:
            player["y"] = player["y"] - Player.SIZE_BODY_RECT[1]


        body = pg.Rect(player["x"], player["y"], Player.SIZE_BODY_RECT[0], Player.SIZE_BODY_RECT[1])


        for brock in cls.bricks:
            if not body.colliderect(brock.rect):
                continue

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