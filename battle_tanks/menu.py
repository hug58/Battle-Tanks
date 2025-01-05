import sys
from typing import Dict, Union
import pygame as pg

from battle_tanks.components.text import TextComponent
from battle_tanks.game import Game
from battle_tanks.commons.package import Struct
from battle_tanks.commons.tank_surface import tank_cover
from battle_tanks.components.network import NetworkComponent

GREEN_STATUS = (0, 128, 0)
RED_STATUS = (255,0,0)
NEU = (100,100,100)
BACKGROUND = (0,30,0)

class Menu:


    def __init__(self, main_surface: pg.Surface):
        self.select_option = None
        self.position:int = 0
        self.main_surface = main_surface
        self.clock = pg.time.Clock()
        self.cover = None
        self.angle = 0
        self.angle_cannon = 0

        self.options:Dict[int,dict] =  {
            # 1:{
            #     "text_draw": Text((200,100),"TESTING MODE", font_size=45, color=NEU),
            #     "action": "SINGLE_PLAYER_MODE"
            # },
            2:{
                "text_draw": TextComponent((260,200),"MULTIPLAYER MODE", font_size=45, color=NEU),
                "action": "MULTIPLAYER_MODE"
            },
        }


    def multiplayer_mode(self,game_screen) -> Union[Game, None]:
        """ Menu mode """
        user_enter = False
        ip_text = "localhost"
        name:str = "JOHN"
        user_text =  "8010"
        option_select = 0
        status =  NEU

        while user_enter is not True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_DOWN:
                        option_select -= 1
                        if option_select < 0:
                            option_select = 0

                    if event.key == pg.K_UP:
                        option_select += 1
                        if option_select > 2:
                            option_select = 2

                    if event.key ==  pg.K_BACKSPACE:
                        if option_select == 2:
                            name = name[:-1]
                        elif option_select == 1:
                            ip_text = ip_text[:-1]
                        else:
                            user_text = user_text[:-1]

                    elif event.key ==  pg.K_RETURN:
                        try:
                            if len(user_text) > 0 and len(name) > 0:
                                check_name = NetworkComponent.check_name((ip_text, int(user_text)), name)
                                if check_name:
                                    game = Game((ip_text, int(user_text)),game_screen, name)
                                    if game.network.player_data != Struct.USER_NOT_AVAILABLE:
                                        return game
                                else:
                                    status = RED_STATUS

                        except ConnectionRefusedError as e:
                            print(e)
                            status = RED_STATUS

                    else:
                        if len(user_text) <= 7:
                            if option_select == 2:
                                name += event.dict.get("unicode")
                                name = name.upper()

                            elif option_select == 1:
                                ip_text += event.dict.get("unicode")
                            elif option_select == 0:
                                try:
                                    user_text += str(int(event.dict.get("unicode")))
                                except ValueError:
                                    pass


                    if event.key != pg.K_DOWN and event.key != pg.K_UP:
                        if len(name) > 0 and option_select == 2:
                            try:
                                port = int(user_text)
                                if 0 < port < 65535:
                                    check_name = NetworkComponent.check_name((ip_text, int(user_text)), name)
                                    if check_name is True:
                                        status = GREEN_STATUS
                                    elif check_name is False:
                                        status = RED_STATUS
                                    else:
                                        print(f"SOCKET NOT CONNECT: {check_name}")
                                        status = NEU
                            except ValueError as e:
                                print(f"ERROR VALUE: {e}")


            self.main_surface.fill(BACKGROUND)

            surface_input_port = pg.Surface((250,40))
            surface_input_ip = pg.Surface((250,40))
            surface_input_name = pg.Surface((250,40))

            text_input = TextComponent((50,20), user_text, (255,255,255))
            text_input.draw(surface_input_port)
            text_input_ip = TextComponent((100,20), ip_text, (255,255,255))
            text_input_ip.draw(surface_input_ip)

            text_input_name = TextComponent((50,20), name, (255,255,255))
            pg.draw.circle(surface_input_name, status, (230, 20), 15)
            text_input_name.draw(surface_input_name)

            text_name = TextComponent((70,60), "NAME: ")
            text_ip = TextComponent((70,120), "IP: ")
            text_port = TextComponent((70,180), "PORT: ")
            text_enter = TextComponent((70,240), "ENTER", status)

            if option_select == 2:
                text_name.color = (255,255,255)
                text_ip.color   = NEU
                text_port.color = NEU
            elif option_select == 1:
                text_ip.color   = (255,255,255)
                text_port.color = NEU
                text_name.color = NEU
            else:
                text_port.color = (255,255,255)
                text_ip.color = NEU
                text_name.color = NEU

            """
            LABELS: IP, PORT AND NAME
            """
            text_ip.draw(self.main_surface)
            text_port.draw(self.main_surface)
            text_name.draw(self.main_surface)
            text_enter.draw(self.main_surface)

            """
            INPUT
            """
            self.main_surface.blit(surface_input_port, (120,160))
            self.main_surface.blit(surface_input_ip, (120,100))
            self.main_surface.blit(surface_input_name,(120,40))

            """
            TANK
            """
            self.angle += 0.5
            self.angle_cannon -= 0.5

            self.angle = self.angle % 360
            self.angle_cannon = self.angle_cannon % 360

            tank_cover(0, (150, 300), self.main_surface, scale=(200, 200), angle=self.angle, angle_cannon=self.angle_cannon)
            tank_cover(1, (450, 300), self.main_surface, scale=(200, 200), angle=self.angle, angle_cannon=self.angle_cannon)

            pg.display.flip()
            self.clock.tick(60)


        return None


    def single_local_mode(self) -> Game:
        """ Single local game """
        return Game(None, self.main_surface, "John")


    def update(self, main_game) -> Game:
        """ getting game state"""
        if len(self.options) == 1:
            self.select_option = [op for op in self.options.keys()][0]
            self.select_option = self.options.get(self.select_option).get("action")

        while self.select_option is None:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    key = event.dict.get('key')

                    if key == pg.K_DOWN or key == pg.K_s:
                        if self.position < len(self.options):
                            self.position +=1

                    if key == pg.K_UP or  key == pg.K_w:
                        if len(self.options) <= self.position:
                            self.position -=1

                    elif key == pg.K_RETURN:
                        select_option: dict = self.options.get(self.position)
                        self.select_option = select_option.get("action")

                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()


            self.draw()
            pg.display.flip()

        return self.multiplayer_mode(main_game) if self.select_option == "MULTIPLAYER_MODE" \
            else self.single_local_mode()


    def draw(self):
        """ Draw options"""
        self.main_surface.fill(BACKGROUND)

        if self.position != 0:
            select_option: dict = self.options.get(self.position)
            text_draw: TextComponent = select_option.get("text_draw")
            text_draw.color=(255,255,255)

            self.options.update({self.position: {
                "text_draw": text_draw,
                "action" : select_option.get("action")
                        }})

        for op,values in self.options.items():
            op_draw = values.get("text_draw")
            if op != self.position:
                op_draw.color=NEU

            op_draw.update()
            op_draw.draw(self.main_surface)

        tank_cover(0,(150,300),self.main_surface,scale=(200,200),angle=0,angle_cannon=0)
        tank_cover(1,(450,300),self.main_surface,scale=(200,200),angle=360,angle_cannon=180)

