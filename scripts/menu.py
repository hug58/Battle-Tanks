"""Menu"""

import pygame as pg
from scripts import Text
from scripts.game import Game

class Menu:
    """Menu """
    def __init__(self):
        self.select_option = None
        self.position:int = 0
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

    def multiplayer_mode(self) -> Game:
        pass

    def draw(self,screen: pg.Surface):
        """ Draw options"""
        key = pg.key.get_pressed()


        if key[pg.K_UP]:
            if (self.position) > 1:
                self.position -=1

        elif key[pg.K_DOWN]:
            if self.position < len(self.options):
                self.position +=1

        elif key[pg.K_RETURN]:
            select_option: dict = self.options.get(self.position)
            self.select_option = select_option.get("action")
        elif key[pg.K_e]:
            self.select_option = None


        if self.position != 0:
            select_option: dict = self.options.get(self.position)
            text_draw: Text = select_option.get("text_draw")
            text_draw.color=(255,255,255)
            # self.options.pop(self.position)
            self.options.update({self.position: {
                "text_draw": text_draw,
                "action" : select_option.get("action")
            }})




        if self.select_option is None:
            screen.fill((0,0,0))

            for op,values in self.options.items():
                op_draw = values.get("text_draw")

                if op != self.position:
                    op_draw.color=(255,0,0)

                # op_draw.update(op)
                op_draw.update()
                op_draw.draw(screen)
