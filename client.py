""" Client and Single Game"""

import pygame as pg
import queue 
import threading as th
import math
from typing import Tuple, List

from battle_tanks.components.text import TextComponent
from battle_tanks import  ROUTE
from battle_tanks.commons.package import Struct
from battle_tanks.components import NetworkComponent
from battle_tanks.menu import Menu


# class Collision:
#     @classmethod
#     def check_collision_bullet(cls, player_data: dict, collision_radius: int) -> dict:
#         """
#         :param player_data: getting x,y and angle_cannon
#         :param collision_radius: radius of collision
#         """
#         bullet_start_pos = cls.calculate_bullet_position(player_data, 0)  # Starting position
#         bullet_end_pos = cls.calculate_bullet_position(player_data, 100)  # End position

#         steps = 10
#         for step in range(steps + 1):
#             t = step / steps
#             bullet_pos = (
#                 bullet_start_pos[0] + t * (bullet_end_pos[0] - bullet_start_pos[0]),
#                 bullet_start_pos[1] + t * (bullet_end_pos[1] - bullet_start_pos[1])
#             )

#             for brick in cls.bricks:
#                 brick: Brick
#                 target_pos = (brick.rect.centerx, brick.rect.centery)
#                 distance = math.sqrt((bullet_pos[0] - target_pos[0]) ** 2 +
#                                      (bullet_pos[1] - target_pos[1]) ** 2)
#                 collided = distance <= collision_radius
#                 if collided:
#                     if isinstance(brick, Brick):
#                         list_game_state: List[bytes] = cls.game_state.split(brick.data)
#                         cls.game_state = b"".join(map(bytes, list_game_state))
#                         brick.remove(cls.bricks)
#                         return {
#                             "type": 5,
#                             "x": brick.rect.x,
#                             "y": brick.rect.y,
#                             "w": brick.rect.w,
#                             "h": brick.rect.h,
#                         }
#                     break  # Eliminar solo el primer bloque en el rango de distancia

#         return {}

#     @staticmethod
#     def calculate_bullet_position(player_data: dict, distance: int) -> Tuple[int, int]:
#         """
#         Calculate the bullet position based on player data and distance.
#         """
#         angle = player_data['angle_cannon']
#         x = player_data['x'] + distance * math.cos(math.radians(angle))
#         y = player_data['y'] + distance * math.sin(math.radians(angle))
#         return x, y


def network_client_consumer(client: NetworkComponent):
    """
    Waits for responses from the server and sends the results to the update queue.
    """
    while True:
        # Receive data from the server
        data = client.recv_move_player()
        
        # Put the received data into the update queue
        NetworkComponent.UPDATE_Q.put(data)


def network_client_handler(client: NetworkComponent):
    """
    Handles network communication for a client.
    """
    while True:
        # Get an item from the SEND_Q queue
        data = NetworkComponent.SEND_Q.get()
        
        # If the item is not queue.Empty, send the move to the server
        if data is not queue.Empty:
            client.send_move_tcp(data)
        


def main():
    """ Client game of server"""

    pg.display.set_caption(f"Battle Tank")
    pg.display.set_icon(pg.image.load(ROUTE("lemon.ico")))
    pg.font.init()
    pg.event.set_allowed([
        pg.QUIT,
        pg.KEYDOWN,
        pg.KEYUP,
    ])

    clock = pg.time.Clock()
    WIDTH,HEIGHT = 800, 600
    SCREEN = pg.display.set_mode((WIDTH,HEIGHT + 36))

    main_game = pg.Surface((WIDTH,HEIGHT))
    menu = Menu(SCREEN)
    game = menu.update(main_game)
    text_damage = TextComponent((WIDTH//2,HEIGHT +16 ),f"Damage: {game.damage} %")
    bullets = pg.Surface((WIDTH,36))



    """
    CLIENT NETWORK
    """
    th_recevied = th.Thread(target = network_client_consumer, daemon = True, args= (game.network,))
    th_send = th.Thread(target = network_client_handler, daemon = True, args=(game.network,))

    th_recevied.start()
    th_send.start()




    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game.close()
            elif event.type == pg.KEYUP:
                key = event.dict.get("key")
                if key == pg.K_o and menu.select_option is not None:
                    if game.player.check_available_bullets():
                        game.player.fire = True
                        game.network.send_move_tcp(Struct.FIRE_EVENT_PLAYER)

            
        SCREEN.fill((0,0,0))
        game.update()
        game.draw(SCREEN)

        bullets.fill((0,50,0))
        game.player.type_gun.render(bullets)
        SCREEN.blit(bullets,(0,HEIGHT))


        text_damage.text = f"Damage: {game.damage} %"
        text_damage.update()
        text_damage.draw(SCREEN)

        """
        TICKS IN CLIENT
        """
        clock.tick(60)
        pg.display.flip()

if __name__ == "__main__":
    main()
