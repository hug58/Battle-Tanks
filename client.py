""" Client and Single Game"""

import pygame as pg
from battle_tanks.components.text import TextComponent
from battle_tanks import  ROUTE
from battle_tanks.commons.package import Struct
from battle_tanks.menu import Menu


def load_bullet(bullet):
    """ load image from file """
    return pg.image.load(ROUTE(bullet[0])),bullet[1]

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
    WIDTH,HEIGHT = 800,600
    SCREEN = pg.display.set_mode((WIDTH,HEIGHT + 36))

    main_game = pg.Surface((WIDTH,HEIGHT))
    menu = Menu(SCREEN)
    game = menu.update(main_game)

    text_damage = TextComponent((WIDTH//2,HEIGHT +16 ),f"Damage: {game.damage} %")
    bullets = pg.Surface((WIDTH,36))

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

        game.update()
        game.draw()

        SCREEN.blit(pg.transform.scale(main_game,(WIDTH,HEIGHT)),(0,0))

        bullets.fill((0,50,0))
        game.player.type_gun.render(bullets)
        SCREEN.blit(bullets,(0,HEIGHT))

        text_damage.text = f"Damage: {game.damage} %"
        text_damage.update()
        text_damage.draw(SCREEN)

        """
        TICKS IN CLIENT
        """
        clock.tick(40)
        pg.display.flip()

if __name__ == "__main__":
    main()
