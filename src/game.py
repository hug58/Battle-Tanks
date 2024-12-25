#!/usr/bin/python3
""" this is the manager game """

import math
from typing import Tuple, Dict, Union, List
import pygame as pg

from src.commons.package import Struct
from src.components.movement import MovementComponent
from src.components.tile_map import TileMap
from src.components.camera import CameraComponent
from src.sprites import Player, Bullet, Brick

from src.commons.municion import CannonType
from src.commons.tank_surface import (create_tank_surface, create_cannon_surface, colors)
from src.components.network import NetworkComponent
from src import ROUTE

TANK = {
    i: {
        0: pg.transform.scale(create_tank_surface(value), (30, 30)),
        1: pg.transform.scale(create_cannon_surface(value), (6 * 2, 16 * 2))
    }
    for i, value in colors.items()
}


type_guns = {
    "MEDIUM": CannonType(10,'ASSETS/images/bullets/bullet_basic.png',(8,10)),
    "BIG": CannonType(10,'ASSETS/images/bullets/big_bullet.png',(8,10)),
    "BASIC": CannonType(10,'ASSETS/images/bullets/bullet_medium.png',(7,8))
}


def _add_obj(obj, player: Player):
    position = player.rect_cannon.center
    return obj(position, player.angle_cannon, player.player_number)


class Game:
    """Class representing Game objects"""
    def __init__(self,addr:Union[Tuple[str,int], None],
                 lvl_map,
                 screen:pg.Surface,
                 player_name="John"):

        self.network = NetworkComponent(addr,player_name) if addr is not None else None
        self._player_number = self.network.player_number if addr is not None else 0
        self.positions = {}

        pg.display.set_caption(f"Lemon Tank - Client: {self._player_number} - User: {player_name}")
        pg.display.set_icon(pg.image.load(ROUTE("lemon.ico")))

        self.WIDTH,self.HEIGHT = screen.get_size()
        self.SCREEN = screen

        self.tile = TileMap(lvl_map)
        self.tile_image = self.tile.make_map()
        self.tile_rect = self.tile_image.get_rect()

        self._players: Dict[int,Player] = {}
        self._bricks = pg.sprite.Group()
        self._bullets = pg.sprite.Group()
        self._damage = 0
        self.load()


        if (self.network and
                self.network.player_data != Struct.USER_NOT_AVAILABLE):
            position = (self.network.player_data["x"],self.network.player_data["y"])
        else:
            position = self.positions[self._player_number]

        self.player = Player(position, self._player_number, cannon_type=type_guns.get("BASIC"))
        self._players[self._player_number] = self.player
        self.camera = CameraComponent(self.tile.WIDTH, self.tile.HEIGHT, (self.WIDTH, self.HEIGHT))
        self.move = MovementComponent(self.network, self.player)


    @property
    def damage(self):
        """ return damage from player """
        return self.player.damage

    def load(self):
        """Load blocks, positions and players """
        for tile_object in self.tile.tmxdata.objects:
            if tile_object.name == 'player':
                self.positions[tile_object.id] = (tile_object.x,tile_object.y)
            elif tile_object.name == 'brick':
                block = Brick(tile_object.x,tile_object.y,tile_object.width,tile_object.height)
                self._bricks.add(block)

    def update(self):
        """ Update Game"""
        self.camera.update(self.player)

        for key,player in self._players.items():
            if player.fire:
                self._bullets.add(_add_obj(Bullet, player))
                player.fire = False

        for bullet in self._bullets:
            self._collided_bullet(bullet)
            bullet.update()
            self._collided_bullet_with_player(bullet)

        self._collided_player(self.player)

        if self.player.fire:
            self._bullets.add(_add_obj(Bullet, self.player))
            self.player.fire = False


        """ SEND MOVES BYTES """
        self.move.keys()
        if self.network:
            recv_all:List[dict] = self.network.recv_move_player()

            for recv in recv_all:
                if recv.get("status") == Struct.NEW_PLAYER:
                    position = recv["position"]
                    pos = (recv["x"],recv["y"])

                    player = Player(pos,position,cannon_type = type_guns.get("BASIC"))
                    self._players[position] = player

                elif recv.get("status") == Struct.UPDATE_PLAYER:
                    position = recv["position"]

                    if self._players.get(position):
                        player = self._players[position]


                        player.rect.x = recv["x"]
                        player.rect.y = recv["y"]

                        # player.body_rect.x = player.rect.x
                        # player.body_rect.y = player.rect.y

                        player.rect_cannon.x = player.rect.x
                        player.rect_cannon.y = player.rect.y

                        player.angle = recv["angle"]
                        player.angle_cannon = recv["angle_cannon"]

                    else:
                        pos = (recv["x"], recv["y"])
                        player = Player(pos, position, cannon_type=type_guns.get("BASIC"))
                        self._players[position] = player

        sprites = pg.sprite.groupcollide(self._bricks,self._bullets,1,0)
        if sprites:
            for sprite, bullets in sprites.items():
                if isinstance(sprite,Brick):
                    for bullet in bullets:
                        if isinstance(bullet,Bullet):
                            bullet.explosion = True

        for brock in self._bricks:
            width_rect = self.player.rect.w * self.player.rect.w
            height_rect = self.player.rect.h * self.player.rect.h

            radius_player = math.sqrt( width_rect  + height_rect ) / 2.0

            width_block = brock.rect.w * brock.rect.w
            height_block = brock.rect.h * brock.rect.h

            radius_block = math.sqrt(width_block + height_block) / 2.0
            radius_sum = radius_block + radius_player

            dx =  brock.rect.right / 2 -( self.player.rect.right / 2)
            dy =  brock.rect.bottom / 2 - (self.player.rect.bottom / 2)

            distance = math.sqrt(dx* dx  + dy*dy )
            separation = radius_sum - distance

            if self.player.rect.colliderect(brock.rect):
                if distance >= radius_sum:
                    pass

                if distance != 0:
                    dx /= distance
                    dy /= distance
                    self.player.rect.x -= dx * separation * 0.125
                    self.player.rect.y -= dy  * separation * 0.125

    def draw(self):
        """ Draw the player and scene. """
        self.SCREEN.blit(self.tile_image,self.camera.apply_rect(self.tile_rect))

        for _,player in self._players.items():
            tank_surface = player.draw(TANK[player.player_number][0], player.angle)
            cannon_surface = player.draw(TANK[player.player_number][1], player.angle_cannon)
            self.SCREEN.blit(tank_surface,self.camera.apply(player))
            self.SCREEN.blit(cannon_surface,self.camera.apply_rect(player.rect_cannon))

        for brick in self._bricks:
            self.SCREEN.blit(brick.image,self.camera.apply(brick))

        for bullet in self._bullets:
            self.SCREEN.blit(bullet.image,self.camera.apply(bullet))

    def _collided_player(self,player):
        if player.rect.left <= 0:
            player.rect.left = 0 
        elif player.rect.right >= self.tile.WIDTH:
            player.rect.right = self.tile.WIDTH

        if player.rect.top <= 0:
            player.rect.top = 0
        elif player.rect.bottom >= self.tile.HEIGHT:
            player.rect.bottom = self.tile.HEIGHT

    def _collided_bullet(self,bullet):
        if bullet.rect.left <= 32 or bullet.rect.right >= (self.tile.WIDTH - 32):
            if bullet.done is not True:
                bullet.explosion = True

    def _collided_bullet_with_player(self,bullet:Bullet):
        if self._player_number != bullet.player_number:
            if self.player.body_rect.colliderect(bullet.rect):
                self.player.damage = self.player.damage + 2.5
                bullet.kill()
        else:
            for _,player in self._players.items():
                if player.body_rect.colliderect(bullet.rect):
                    bullet.explosion = True
                    break

    def _collided_object_with_player(self, object):
        if self.player.body_rect.colliderect(object.rect):
            if self.player.rect.left <= object.rect.left:
                self.player.rect.left = object.rect.left
            elif self.player.rect.right >= object.rect.right:
                self.player.rect.right = object.rect.left
            if self.player.rect.top <= object.rect.top:
                self.player.rect.top = object.rect.top
            elif self.player.rect.bottom >= object.rect.bottom:
                self.player.rect.bottom = object.rect.bottom

    def __str__(self):
        return (f"\n\nPlayer Number: {self._player_number} "
                f"\nPlayer Name: {self.network.name} "
                f"\nStatus: {'Multiplayer' if self.network.addr else 'Single'}\n\n")