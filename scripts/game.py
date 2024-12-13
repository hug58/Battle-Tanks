#!/usr/bin/python3
""" this is the manager game """

import math
from typing import Tuple,Dict
import pygame as pg

from scripts.commons.package import Struct
from scripts.tile_map import TileMap
from scripts.camera import Camera
from scripts.sprites import Player,Bullet, Brick

from scripts.commons.municion import CannonType
from scripts.commons.tank_surface import create_tank_surface, colors

from scripts.network import Client
from scripts import ROUTE


TANK = {}

for i,value in colors.items():
    _tank = create_tank_surface(value)
    cannon = pg.image.load(ROUTE(f'ASSETS/images/c_0{0}.png'))
    TANK[i] = {
        0:pg.transform.scale(_tank,(30,30)),
        1:pg.transform.scale(cannon,(8*2,16*2))
    }

type_guns = {
    "MEDIUM": CannonType(10,'ASSETS/images/bullets/bullet_basic.png',(8,10)),
    "BIG": CannonType(10,'ASSETS/images/bullets/big_bullet.png',(8,10)),
    "BASIC": CannonType(10,'ASSETS/images/bullets/bullet_medium.png',(7,8))
}


class Game(Client):
    """Class representing Game objects"""

    def __init__(self,addr:Tuple[str,int],lvl_map,screen, player_name="John"):
        Client.__init__(self,addr,player_name)
        self._number_player = self.player_number if addr is not None else 0

        pg.display.set_caption(f"Lemon Tank - Client {self._number_player} - User: {player_name}")
        pg.display.set_icon(pg.image.load(ROUTE('lemon.ico')))

        self.WIDTH,self.HEIGHT = screen.get_size()
        self.SCREEN = screen
        self.tile = TileMap(lvl_map)
        self.tile_image = self.tile.make_map()
        self.tile_rect = self.tile_image.get_rect()

        self._players: Dict[int,Player] = {}
        self._damage = 0

        self._bricks = pg.sprite.Group()
        self._bullets = pg.sprite.Group()

        #LOAD POSITIONS PLAYERS AND BLOCKS
        self.load()

        position = (self.player_data["x"],self.player_data["y"])
        print(f"POSITION: {position}")

        self.player = Player(position, cannon_type=type_guns.get("BASIC"))
        self.player._num_player = self._number_player
        self._players[self._number_player] = self.player
        self.camera = Camera(self.tile.WIDTH,self.tile.HEIGHT,(self.WIDTH,self.HEIGHT))


    @property
    def damage(self):
        """ return damage from player """
        return self.player.damage


    def load(self):
        """Load blocks, positions and players """
        for tile_object in self.tile.tmxdata.objects:
            if tile_object.name == 'player':
                pass
                # self.POSITIONS[tile_object.id] = (tile_object.x,tile_object.y)
            elif tile_object.name == 'brick':
                block: pg.sprite.Sprite = Brick(tile_object.x,tile_object.y,tile_object.width,tile_object.height)
                self._bricks.add(block)


    def update(self):
        """ Update Game"""
        self.camera.update(self.player)


        for key,player in self._players.items():

            if player.fire:
                self._bullets.add(self._add_obj(Bullet,player))
                player.fire = False

        for bullet in self._bullets:
            self._collided_bullet(bullet)
            bullet.update()
            self._collided_bullet_with_player(bullet)

        self._collided_player(self.player)

        if self.player.fire:
            self._bullets.add(self._add_obj(Bullet,self.player))
            self.player.fire = False


        """ SEND MOVES BYTES """
        self._move()
        recv:dict = self.recv_move_player()


        if recv.get("status") == Struct.NEW_PLAYER:
            print(f"NUEVO JUGADOR {recv['position']}")
            position = recv["position"]
            pos = (recv["x"],recv["y"])

            player = Player(pos,cannon_type = type_guns.get("BASIC"))
            player.number_player = position
            self._players[position] = player

        elif recv.get("status") == Struct.UPDATE_PLAYER:
            print("VIEJO JUGADOR")

            position = recv["position"]
            player = self._players[position]

            player.rect.x = recv["x"]
            player.rect.y = recv["y"]

            player.rect_cannon.x = recv["cannon_x"]
            player.rect_cannon.y = recv["cannon_y"]

            player.angle = recv["angle"]
            player.angle_cannon = recv["angle_cannon"]




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
            dy =   brock.rect.bottom / 2 - (self.player.rect.bottom / 2)

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

        self.camera.update(self.player)


    def _move(self):
        key = pg.key.get_pressed()

        if key[pg.K_d]:
            self.send_move(Struct.RIGHT_EVENT_PLAYER)

            # self.player.rotate_rect(-1, TANK[self._number_player][0])
            # self.player.angle_cannon,self.player.rect_cannon = Player.rotate_external(-1,
            # self.player.angle_cannon,TANK[self._number_player][1],self.player.rect_cannon)

        elif key[pg.K_a]:
            self.send_move(Struct.LEFT_EVENT_PLAYER)

            # self.player.rotate_rect(1, TANK[self._number_player][0])
            # self.player.angle_cannon,self.player.rect_cannon = Player.rotate_external(1,
            # self.player.angle_cannon,TANK[self._number_player][1],self.player.rect_cannon)

        radians = math.radians(self.player.angle)
        self.player.vlx = self.player.vl * - math.sin(radians)
        self.player.vly = self.player.vl * - math.cos(radians)

        if key[pg.K_w]:
            self.send_move(Struct.UP_EVENT_PLAYER)


        if key[pg.K_s]:
            self.send_move(Struct.DOWN_EVENT_PLAYER)
            # self.player.rect.centerx -= self.player.vlx
            # self.player.rect.centery -= self.player.vly

        # self.player.body_rect.center = self.player.rect.center
        # self.player.rect_cannon.center = self.player.body_rect.center

        if key[pg.K_i]:
            self.send_move(Struct.LEFT_ANGLE_EVENT_PLAYER)
            # self.player.angle_cannon,self.player.rect_cannon = Player.rotate_external(1,
            # self.player.angle_cannon,TANK[self._number_player][1],self.player.rect_cannon)

        elif key[pg.K_p]:
            self.send_move(Struct.RIGHT_ANGLE_EVENT_PLAYER)

            # self.player.angle_cannon,self.player.rect_cannon = Player.rotate_external(-1,
            # self.player.angle_cannon,TANK[self._number_player][1],self.player.rect_cannon)


    def draw(self):
        """ Draw the player and scene. """

        self.SCREEN.blit(self.tile_image,self.camera.apply_rect(self.tile_rect))

        for _,player in self._players.items():
            tank_surface = player.draw(TANK[player.number_player][0], player.angle)
            cannon_surface = player.draw(TANK[player.number_player][1], player.angle_cannon)
            self.SCREEN.blit(tank_surface,self.camera.apply(player))
            self.SCREEN.blit(cannon_surface,self.camera.apply_rect(player.rect_cannon))

        for brick in self._bricks:
            self.SCREEN.blit(brick.image,self.camera.apply(brick))


        # main_tank = self.player.draw(TANK[self._number_player][0],self.player.angle)
        # main_cannon = self.player.draw(TANK[self._number_player][1],self.player.angle_cannon)
        # self.SCREEN.blit(main_tank,self.camera.apply(self.player))
        # self.SCREEN.blit(main_cannon,self.camera.apply_rect(self.player.rect_cannon))
        # pg.draw.rect(self.SCREEN,(0,100,0),self.camera.apply_rect(self.player.rect),1)
        # pg.draw.rect(self.SCREEN,(100,0,0),self.camera.apply_rect(self.player.body_rect),1)

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


    def _add_obj(self,obj, player: Player):
        position = player.rect_cannon.center
        return obj(position, player.angle_cannon, player.number_player)


    def _collided_bullet(self,bullet):
        if bullet.rect.left <= 32 or bullet.rect.right >= (self.tile.WIDTH - 32):
            if bullet.done is not True:
                bullet.explosion = True


    def _collided_bullet_with_player(self,bullet):
        if self._number_player != bullet.num_player:
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
        return (f"\n\nPlayer Number: {self.player_number} "
                f"\nPlayer Name: {self.name} "
                f"\nStatus: {'Multiplayer' if self.addr else 'Single'}\n\n")