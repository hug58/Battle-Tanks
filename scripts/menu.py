"""Menu"""

import sys
import socket
import pygame as pg
from scripts import Text
from scripts.game import Game
from scripts.commons.package import JOIN_MESSAGE,OK_MESSAGE,BUFFER_SIZE_INIT_PLAYER

class Menu:
    """Menu """
    def __init__(self, main_surface: pg.Surface, map_tmp:str):
        self.select_option = None
        self.position:int = 0
        self.main_surface = main_surface
        self.map_tmp = map_tmp
        self.clock = pg.time.Clock()
        self.options:dict =  {
            1:{
                "text_draw": Text((70,100),"TESTING MODE"),
                "action": "SINGLE_PLAYER_MODE"
            },
            2:{
                "text_draw": Text((100,200),"MULTIPLAYER MODE"),
                "action": "MULTIPLAYER_MODE"
            },
        }


    def multiplayer_mode(self,game_screen) -> Game:
        """ Menu mode """
        user_enter = False
        ip_text = "localhost"
        user_text =  "8010"
        option_select = 0

        while user_enter is not True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_DOWN:
                        option_select = 1

                    if event.key == pg.K_UP:
                        option_select = 0

                    if event.key ==  pg.K_BACKSPACE:
                        if option_select == 1:
                            user_text = user_text[:-1]
                        else:
                            ip_text = ip_text[:-1]
                    elif event.key ==  pg.K_RETURN:
                        try:
                            if len(user_text) > 0:
                                _socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                                _socket.connect((ip_text, int(user_text)))
                                _socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
                                ok = _socket.recv(BUFFER_SIZE_INIT_PLAYER)
                                _socket.send(JOIN_MESSAGE)
                                if ok == OK_MESSAGE:
                                    user_enter = True
                                    _socket.close()

                        except ConnectionRefusedError as e:
                            print(e)

                    else:
                        if len(user_text) <= 7:
                            if option_select == 1:
                                user_text += event.dict.get("unicode")
                            else:
                                ip_text += event.dict.get("unicode")

            self.main_surface.fill((0,50,0))
            surface_input = pg.Surface((100,40))
            surface_input_ip = pg.Surface((110,40))

            text_input = Text((50,20), user_text, (255,255,255))
            text_input.draw(surface_input)

            text_input_ip = Text((55,20), ip_text, (255,255,255))
            text_input_ip.draw(surface_input_ip)

            text_ip = Text((70,60), "IP: ")
            text_port = Text((70,120), "PORT: ")
            text_enter = Text((240,120), "ENTER", (255,255,255))

            if option_select == 0:
                text_ip.color = (255,255,255)
                text_port.color = (255,0,0)
            else:
                text_ip.color = (255,0,0)
                text_port.color = (255,255,255)

            text_ip.draw(self.main_surface)
            text_port.draw(self.main_surface)
            text_enter.draw(self.main_surface)
            self.main_surface.blit(surface_input, (100,100))
            self.main_surface.blit(surface_input_ip, (100,40))


            pg.display.flip()
            self.clock.tick(60)



        return Game((ip_text, int(user_text)), self.map_tmp, game_screen)


    def single_local_mode(self, game_screen) -> Game:
        """ Single local game """
        return Game(None,self.map_tmp,game_screen)



    def  update(self, main_game) -> Game:
        """ getting game state"""
        print("init")
        while self.select_option is None:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:

                    key = event.dict.get('key')
                    if key == pg.K_DOWN:
                        if self.position < len(self.options):
                            self.position +=1


                    if key == pg.K_UP:
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

        game_select = None
        if self.select_option == "MULTIPLAYER_MODE":
            game_select = self.multiplayer_mode(main_game)
        else:
            game_select = self.single_local_mode(main_game)

        print("FUN")
        return game_select



    def draw(self):
        """ Draw options"""
        self.main_surface.fill((0,0,0))

        if self.position != 0:
            select_option: dict = self.options.get(self.position)
            text_draw: Text = select_option.get("text_draw")
            text_draw.color=(255,255,255)
            # self.options.pop(self.position)
            self.options.update({self.position: {
                "text_draw": text_draw,
                "action" : select_option.get("action")
                        }})

        for op,values in self.options.items():
            op_draw = values.get("text_draw")
            if op != self.position:
                op_draw.color=(255,0,0)

                # op_draw.update(op)
            op_draw.update()
            op_draw.draw(self.main_surface)
