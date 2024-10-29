import pygame as pg 
import math

from .. import ROUTE
from .animation import Animation


class Bullet(pg.sprite.Sprite,Animation):
    """it represents a projectile """
    def __init__(self,position,angle,num_player):
        pg.sprite.Sprite.__init__(self)
        explosion = pg.image.load(ROUTE(f'ASSETS/images/explosion_bullet_0{num_player}.png'))
        explosion = pg.transform.scale(explosion,(16,48))
        size_e = (16,16)
        frames = {0:((0,0),size_e),1:((0,16),size_e),2:((0,32),size_e)}
        Animation.__init__(self,explosion,frames)
        self.image = pg.Surface((4,8))
        self.image = pg.transform.rotate(self.image,angle)
        self.rect = self.image.get_rect()
        self.vl = 20
        self.rect.center = position
        self.radians = math.radians(angle)
        self.rect.centerx +=  math.sin(self.radians) * -30 
        self.rect.centery +=  math.cos(self.radians) * -30
        self.vlx = self.vl * - math.sin(self.radians)
        self.vly = self.vl * - math.cos(self.radians)
        self.explosion = False 
        self.num_player = num_player
        self._delay = 2

        self.image.fill((2,218,136)) if num_player == 0 else self.image.fill((188,2,218))


    def update(self):
        """ update bullet position and status"""

        if self.explosion is not True:
            self.rect.centerx += self.vlx
            self.rect.centery += self.vly
        else:
            self._update()
            rect = self.image.get_rect()
            rect.center = self.rect.center
            self.rect = rect
            if self.done:
                self.kill()

    def draw(self,screen):
        """ draw bullet in windows"""
        screen.blit(self.image,self.rect)

