""" Client and Single Game"""

import sys
import pygame as pg
from src import Text, ROUTE
from src.menu import Menu


def load_bullet(bullet):
    """ load image from file """
    return pg.image.load(ROUTE(bullet[0])),bullet[1]

def main():
    """ Client game of server"""

    map_tmp = "ASSETS/maps/zone_0.tmx"
    WIDTH,HEIGHT = 800,600
    SCREEN = pg.display.set_mode((WIDTH,HEIGHT + 36))
    clock = pg.time.Clock()
    main_game = pg.Surface((600,400))
    menu = Menu(SCREEN,map_tmp)

    pg.display.set_caption(f"Lemon Tank")
    pg.display.set_icon(pg.image.load(ROUTE("lemon.ico")))

    game = menu.update(main_game)

    text_damage = Text((WIDTH//2,HEIGHT +16 ),f"Damage: {game.damage} %")
    bullets = pg.Surface((WIDTH,36))

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                game.network.socket_tcp.close()
                sys.exit()

            if event.type == pg.KEYUP:
                key = event.dict.get("key")
                if key == pg.K_o and menu.select_option is not None:
                    if game.player.check_available_bullets():
                        game.player.fire = True


        text_damage.text = f"Damage: {game.damage} %"
        text_damage.draw(SCREEN)

        game.update()
        game.draw()

        SCREEN.blit(pg.transform.scale(main_game,(WIDTH,HEIGHT)),(0,0))
        SCREEN.blit(bullets,(0,HEIGHT))
        bullets.fill((0,0,0))
        bullets_renders = list(map(load_bullet,game.player.type_gun.render()))
        bullets.blits(bullets_renders)

        """
        TICKS IN CLIENT
        """
        clock.tick(30)
        pg.display.flip()

if __name__ == "__main__":
    main()
