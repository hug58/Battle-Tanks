import pygame as pg
from typing import Union
from src.components.network import NetworkComponent
from src.sprites import Player
from src.commons.package import (Struct,)




class MovementComponent:
    """
        MOVES GAME COMPONENT
    """
    def __init__(self, network: Union[NetworkComponent,None], player:Player):
        self.network = network
        self.player = player


    def keys(self):
        key = pg.key.get_pressed()
        action = None

        if key[pg.K_d]:
            action = Struct.RIGHT_EVENT_PLAYER
            # self.player.rotate_rect(-1, Player.TANK[self.player.number_player][0])
            # self.player.angle_cannon, self.player.rect_cannon = Player.rotate_external(
            #     -1, self.player.angle_cannon, Player.TANK[self.player.number_player][1], self.player.rect_cannon
            # )

        elif key[pg.K_a]:
            action = Struct.LEFT_EVENT_PLAYER
            # self.player.rotate_rect(1, Player.TANK[self.player.number_player][0])
            # self.player.angle_cannon, self.player.rect_cannon = Player.rotate_external(
            #     1, self.player.angle_cannon, Player.TANK[self.player.number_player][1], self.player.rect_cannon
            # )

        elif key[pg.K_w]:
            action = Struct.UP_EVENT_PLAYER
            # radians = math.radians(self.player.angle)
            # self.player.vlx = self.player.vl * -math.sin(radians)
            # self.player.vly = self.player.vl * -math.cos(radians)
            # self.player.rect.centerx += self.player.vlx
            # self.player.rect.centery += self.player.vly

        elif key[pg.K_s]:
            action = Struct.DOWN_EVENT_PLAYER
            # radians = math.radians(self.player.angle)
            # self.player.vlx = self.player.vl * -math.sin(radians)
            # self.player.vly = self.player.vl * -math.cos(radians)
            # self.player.rect.centerx -= self.player.vlx
            # self.player.rect.centery -= self.player.vly

        elif key[pg.K_i]:
            action = Struct.LEFT_ANGLE_EVENT_PLAYER
            # self.player.angle_cannon, self.player.rect_cannon = Player.rotate_external(
            #     1, self.player.angle_cannon, Player.TANK[self.player.number_player][1], self.player.rect_cannon
            # )

        elif key[pg.K_p]:
            action = Struct.RIGHT_ANGLE_EVENT_PLAYER
            # self.player.angle_cannon, self.player.rect_cannon = Player.rotate_external(
            #     -1, self.player.angle_cannon, Player.TANK[self.player.number_player][1], self.player.rect_cannon
            # )

        # elif key[pg.K_o]:
        #     if self.player.check_available_bullets():
        #         action = Struct.FIRE_EVENT_PLAYER
        #         self.player.fire = True

        # self.player.body_rect.center = self.player.rect.center
        # self.player.rect_cannon.center = self.player.body_rect.center


        if self.network and action:
            self.network.send_move_tcp(action)


