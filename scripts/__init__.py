""" Commons """

import os.path
import sys
from typing import Tuple
import pygame as pg

pg.font.init()

def resolve_route(rute,relative = '.'):
    """resolve_route"""
    if hasattr(sys,'_MEIPASS'):
        return os.path.join(sys._MEIPASS,rute)
    return os.path.join(os.path.abspath(relative),rute)


ROUTE = lambda route: os.path.join(os.path.abspath("."),route)


class Text:
    """Surface for text rendering """
    def __init__(self,position,text):
        self._font = ROUTE('ASSETS/Pixel Digivolve.otf')
        self._color:Tuple = (255,0,0) #default
        self._surface = self.render(text,self._font,self._color)
        self._rect = self._surface.get_rect()
        self._rect.center = position
        self._text = text

    @staticmethod
    def render(text:str, font: pg.font, color: Tuple[int,int] ):
        """ Render text """
        return pg.font.Font(font,16).render(text,1,color)


    def update(self):
        """ Updates the surface """
        self._surface = self.render(self._text,self._font,self._color)

    @property
    def color(self):
        """getter color"""
        return self._color

    @color.setter
    def color(self,color:Tuple):
        """color set"""
        self._color = color

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
