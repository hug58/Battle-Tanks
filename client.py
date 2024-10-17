""" Client and Single Game"""

import pygame as pg
from scripts import Text
from scripts.game import Game
from scripts.menu import Menu
def main():
    """ Client game of server"""
    # try:
    #     HOST = input("IP SERVER:")
    #     PORT = input("PORT SERVER:")
    #     #HOST = "10.30.0.107"
    # except KeyboardInterrupt:
    #     pass
    HOST="0.0.0.0"
    print('\n')
    map_tmp = 'ASSETS/maps/zone_0.tmx'
    WIDTH,HEIGHT = 800,600
    SCREEN = pg.display.set_mode((WIDTH,HEIGHT + 36))
    clock = pg.time.Clock()
    main_surface = pg.Surface((WIDTH,HEIGHT))


    # game = Game((HOST,int(PORT)),map_tmp,SURFACE)
    game = Game(None,map_tmp,main_surface)
    text_damage = Text((WIDTH//2,HEIGHT +16 ),f'Damage: {game.damage} %')
    bullets = pg.Surface((WIDTH,36))

    menu = Menu()

    while True:
        clock.tick(30)

        SCREEN.fill((0,0,0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                break
            if event.type == pg.KEYUP:
                key = event.dict.get("key")
                if key == pg.K_o and menu.select_option is not None:
                    if game.player.check_available_bullets():
                        game.player.fire = True


        text_damage.text = f'Damage: {game.damage} %'
        text_damage.draw(SCREEN)

        menu.draw(SCREEN)

        if menu.select_option is not None:
            game.update()
            game.draw()
            SCREEN.blit(main_surface,(0,0))
            SCREEN.blit(bullets,(0,HEIGHT))
            bullets.fill((0,0,0))
            bullets.blits(game.player.type_gun.render())




        pg.display.flip()

if __name__ == '__main__':
    main()
    pg.quit()
