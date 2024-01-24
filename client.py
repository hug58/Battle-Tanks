
import pygame as pg
import socket

from scripts import Text
from scripts.game import Game

def main():
    """ Client game of server"""
    try:
        HOST = input("IP SERVER:")
        PORT = input("PORT SERVER:")
        #HOST = "10.30.0.107"
    except KeyboardInterrupt:
        pass
    print(HOST)
    print('\n')
    map_tmp = 'ASSETS/maps/zone_0.tmx'
    WIDTH,HEIGHT = 800,600
    SCREEN = pg.display.set_mode((WIDTH,HEIGHT + 36))
    clock = pg.time.Clock()
    SURFACE = pg.Surface((WIDTH,HEIGHT))
    game = Game((HOST,PORT),map_tmp,SURFACE)
    text_damage = Text((WIDTH//2,HEIGHT +16 ),f'Damage: {game.damage} %')
    
    while True:
        clock.tick(30)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                break
        game.update()
        SCREEN.fill((0,0,0))
        game.draw()	
        text_damage.update(f'Damage: {game.damage} %')
        text_damage.draw(SCREEN)
        SCREEN.blit(SURFACE,(0,0))
        pg.display.flip()

if __name__ == '__main__':
    main()
    pg.quit()
