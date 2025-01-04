""" Commons """

import os.path
import sys
from typing import Tuple
import pygame as pg

pg.font.init()
pg.mixer.init()


def resolve_route(rute,relative = '.'):
    """resolve_route"""
    if hasattr(sys,'_MEIPASS'):
        return os.path.join(sys._MEIPASS,rute)
    return os.path.join(os.path.abspath(relative),rute)


ROUTE = lambda route: os.path.join(os.path.abspath("."), route)
FONT = ROUTE("assets/Pixel Digivolve.otf")

sound_shot = pg.mixer.Sound(ROUTE("assets/sound/shot.wav"))
sound_boom = pg.mixer.Sound(ROUTE("assets/sound/boom.wav"))
sound_boom.set_volume(0.1)



class Text:
    """Surface for text rendering """
    def __init__(self, position, text, color = None, font_size = 16*2):
        self._color:Tuple[int,int,int] = color if color is not None else (255,0,0)  #default
        self.size_font =  font_size
        self._surface = self.render(text,FONT,self._color, self.size_font)
        self._rect = self._surface.get_rect()
        self._rect.center = position
        self._text = text


    @staticmethod
    def render(text:str, font: pg.font, color: Tuple[int,int,int], size):
        """ Render text """
        return pg.font.Font(font,size).render(text,1,color)


    def update(self):
        """ Updates the surface """
        self._surface = self.render(self._text,FONT,self._color, self.size_font)


    @property
    def color(self):
        """getter color"""
        return self._color


    @color.setter
    def color(self,color:Tuple[int,int,int]):
        """color set"""
        self._color = color
        self._surface = self.render(self._text,FONT,self._color, self.size_font)


    @property
    def text(self):
        """getting """
        return self._text


    @text.setter
    def text(self,text):
        """setter """
        self._text = text


    def draw(self,screen):
        """ draw"""
        screen.blit(self._surface,self._rect)
