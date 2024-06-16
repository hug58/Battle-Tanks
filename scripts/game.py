#!/usr/bin/python3

import math
import pygame as pg

from scripts.tile_map import TileMap
from scripts.camera import Camera
from scripts.sprites import Player,Bullet, Brick
from scripts.network import Client
from scripts import ROUTE


from typing import Tuple,Dict
TANK = {}

for i in range(2):
    _tank = pg.image.load(ROUTE(f'ASSETS/images/t_0{i}.png'))
    cannon = pg.image.load(ROUTE(f'ASSETS/images/c_0{i}.png'))
    TANK[i] = {
        # 0:pg.transform.scale(_tank,(64,64)),
        # 1:pg.transform.scale(cannon,(20*2,28*2))
        0:pg.transform.scale(_tank,(30,30)),
        1:pg.transform.scale(cannon,(8*2,16*2))

    }


class Game(Client):
    '''
        Class representing Game objects
    '''
    def __init__(self,addr:Tuple[str,int],lvl_map,SCREEN):
        Client.__init__(self,addr)
        self._number_player = int(self._get_number_player())
        pg.display.set_caption(f"Lemon Tank - Client {self._number_player}")
        pg.display.set_icon(pg.image.load(ROUTE('lemon.ico')))
        
        self.WIDTH,self.HEIGHT = SCREEN.get_size()
        self.SCREEN = SCREEN
        self.tile = TileMap(lvl_map)
        self.tile_image = self.tile.make_map()
        self.tile_rect = self.tile_image.get_rect()

        self._players: Dict[int,Player] = {}
        self.POSITIONS = {}
        self._damage = 0
        self._load()
        self.player = Player(self.POSITIONS[self._number_player])
        self.player._num_player = self._number_player
        self._send(self.player)
        

        if self._data:
            self._players = self._data

        self.camera = Camera(self.tile.WIDTH,self.tile.HEIGHT,(self.WIDTH,self.HEIGHT))
        self._bullets = pg.sprite.Group()

    @property
    def damage(self):
        """ return damage from player """
        return self.player.damage


    def _load(self):
        self._bricks = pg.sprite.Group()

        for tile_object in self.tile.tmxdata.objects:
            if tile_object.name == 'player':
                self.POSITIONS[tile_object.id] = (tile_object.x,tile_object.y)
            elif tile_object.name == 'brick':
                block = Brick(tile_object.x,tile_object.y,tile_object.width,tile_object.height)
                self._bricks.add(block)

            

    def update(self):
        """ Update Game"""
        self.camera.update(self.player)

        if self._data:
            self._players = self._data
        
        for _,player in self._players.items():
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


        self._move()
        self._send(self.player)

        sprites = pg.sprite.groupcollide(self._bricks,self._bullets,1,0)
        if sprites:
            for sprite in sprites.items():
                if isinstance(sprite,Brick):
                    print("It's a brick")

                for bullet in sprite:
                    if isinstance(bullet,Bullet):
                        bullet.explosion = True

            sprites = {}

        # for brock in self._bricks:

        #     widthP = self.player.rect.w * self.player.rect.w
        #     heightP = self.player.rect.h * self.player.rect.h
   
        #     widthO = brock.rect.w * brock.rect.w
        #     heightO = brock.rect.h * brock.rect.h
    
        #     radiusPlayer = math.sqrt( widthP + heightP) / 2.0;
        #     radiusOb = math.sqrt(widthO + heightO) / 2.0;


        #     if self.player.rect.colliderect(brock.rect):
        #         # Calcular la distancia euclidiana
        #         # dx = abs( self.player.rect.x + self.player.rect.w / 2 - (brock.rect.x + brock.rect.w / 2))
        #         dx = abs( brock.rect.x + brock.rect.w / 2 -( self.player.rect.x + self.player.rect.w / 2))
        #         # dy = abs(self.player.rect.y + self.player.rect.h / 2 - (brock.rect.y + brock.rect.h / 2))
        #         dy = abs(  brock.rect.y + brock.rect.h / 2 - (self.player.rect.y + self.player.rect.h / 2))

        #         distance = math.sqrt(dx* dx  + dy*dx )
        #         radiusSum = radiusOb + radiusPlayer;
                
        #         if distance >= radiusSum:
        #             pass 

        #         separation = radiusSum - distance;
        #         if distance != 0:
        #             dx /= distance
        #             dy /= distance
        #             self.player.rect.x -= dx * separation * 0.1
        #             self.player.rect.y -= dy  * separation * 0.1

        self.camera.update(self.player)


    def _move(self):
        key = pg.key.get_pressed()

        if key[pg.K_d]:
            self.player._rotate(-1, TANK[self._number_player][0])
            self.player._angle_cannon,self.player._rect_cannon = self.player.rotate(
                -1,self.player._angle_cannon,TANK[self._number_player][1],self.player._rect_cannon
                )

        elif key[pg.K_a]:
            self.player._rotate(1, TANK[self._number_player][0])

            self.player._angle_cannon,self.player._rect_cannon = self.player.rotate(1,
                self.player._angle_cannon,TANK[self._number_player][1],self.player._rect_cannon
                )


        radians = math.radians(self.player._angle)
        self.player.vlx = self.player._VL * - math.sin(radians)
        self.player.vly = self.player._VL * - math.cos(radians)

        if key[pg.K_w]:

            self.player.rect.centerx += self.player.vlx
            self.player.rect.centery += self.player.vly


        if key[pg.K_s]:

            self.player.rect.centerx -= self.player.vlx
            self.player.rect.centery -= self.player.vly


        self.player._rect_interno.center = self.player.rect.center
        self.player._rect_cannon.center = self.player._rect_interno.center




        if key[pg.K_i]:
            self.player._angle_cannon,self.player._rect_cannon = self.player.rotate(-1,self.player._angle_cannon,
            TANK[self._number_player][1],self.player._rect_cannon
            )

        elif key[pg.K_p]:
            self.player._angle_cannon,self.player._rect_cannon = self.player.rotate(1,self.player._angle_cannon,
            TANK[self._number_player][1],self.player._rect_cannon
            )


        if key[pg.K_o]:
            self.player._fire = True


    def draw(self):
        self.SCREEN.blit(self.tile_image,self.camera.apply_rect(self.tile_rect))

        for _,player in self._players.items():
            tank = player.draw(TANK[player._num_player][0], player._angle)
            cannon = player.draw(TANK[player._num_player][1], player._angle_cannon)
            self.SCREEN.blit(tank,self.camera.apply(player))
            self.SCREEN.blit(cannon,self.camera.apply_rect(player._rect_cannon))

        for brick in self._bricks:
            self.SCREEN.blit(brick.image,self.camera.apply(brick))

        tank = self.player.draw(TANK[self._number_player][0],self.player._angle)
        cannon = self.player.draw(TANK[self._number_player][1],self.player._angle_cannon)
        self.SCREEN.blit(tank,self.camera.apply(self.player))
        self.SCREEN.blit(cannon,self.camera.apply_rect(self.player._rect_cannon))
        pg.draw.rect(self.SCREEN,(0,100,0),self.camera.apply_rect(self.player._rect_interno),1)
        pg.draw.rect(self.SCREEN,(100,0,0),self.camera.apply_rect(self.player._rect_cannon),1)

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


    def _add_obj(self,obj, player):
        position = (player._rect_cannon.center)
        return obj(position, player._angle_cannon, player._num_player)
    

    def _collided_bullet(self,bullet):
        if bullet.rect.left <= 32 or bullet.rect.right >= (self.tile.WIDTH - 32):
            if bullet._done != True:
                bullet.explosion = True


    def _collided_bullet_with_player(self,bullet):
        if self._number_player != bullet._num_player:
            if self.player._rect_interno.colliderect(bullet.rect):
                self.player._damage += 2.5
                bullet.kill()
        else:
            for _,player in self._players.items():
                if player._rect_interno.colliderect(bullet.rect):
                    bullet.explosion = True 
                    break
    
    
    def _collided_object_with_player(self, object):
        if self.player._rect_interno.colliderect(object.rect):
            if self.player.rect.left <= object.rect.left:
                self.player.rect.left = object.rect.left
            elif self.player.rect.right >= object.rect.right:
                self.player.rect.right = object.rect.left
            if self.player.rect.top <= object.rect.top:
                self.player.rect.top = object.rect.top
            elif self.player.rect.bottom >= object.rect.bottom:
                self.player.rect.bottom = object.rect.bottom