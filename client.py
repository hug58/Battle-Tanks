""" Client and Single Game"""

import socket
import sys
import pygame as pg
import asyncio

from scripts import Text, ROUTE
from scripts.menu import Menu


def scan_ports(ip, start_port, end_port):
    """ SCANNING PORTS FOR GAME STATUS """
    print(f"Escaneando puertos en {ip} desde {start_port} hasta {end_port}...")
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Establece un tiempo de espera de 1 segundo
        result = sock.connect_ex((ip, port))  # Intenta conectar al puerto
        if result == 0:
            print(f"Puerto {port} está abierto")
        sock.close()


def load_bullet(bullet):
    """ load image from file """
    return (pg.image.load(ROUTE(bullet[0])),bullet[1])

async def main():
    """ Client game of server"""

    map_tmp = 'ASSETS/maps/zone_0.tmx'
    WIDTH,HEIGHT = 800,600
    SCREEN = pg.display.set_mode((WIDTH,HEIGHT + 36))
    clock = pg.time.Clock()
    main_surface = pg.Surface((WIDTH,HEIGHT))

    menu = Menu(SCREEN,map_tmp)
    game = menu.update(main_surface)

    text_damage = Text((WIDTH//2,HEIGHT +16 ),f'Damage: {game.damage} %')
    bullets = pg.Surface((WIDTH,36))

    while True:
        SCREEN.fill((110,0,0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.KEYUP:
                key = event.dict.get("key")
                if key == pg.K_o and menu.select_option is not None:
                    if game.player.check_available_bullets():
                        game.player.fire = True


        text_damage.text = f'Damage: {game.damage} %'
        text_damage.draw(SCREEN)

        game.update()
        game.draw()
        SCREEN.blit(main_surface,(0,0))
        SCREEN.blit(bullets,(0,HEIGHT))
        bullets.fill((0,0,0))
        bullets_renders = list(map(load_bullet,game.player.type_gun.render()))
        bullets.blits(bullets_renders)
        clock.tick(30)


        pg.display.flip()

if __name__ == '__main__':
    asyncio.run(main())
    pg.quit()
