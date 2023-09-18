import pygame as pg
from scripts import ROUTE

pg.font.init()
RENDER_TEXT = lambda text,font,color: pg.font.Font(font,16).render(text,1,color)


class Text:
	def __init__(self,position,text):
		self._font = ROUTE('ASSETS/Pixel Digivolve.otf')
		self._color = (255,0,0)
		self._surface = RENDER_TEXT(text,self._font,self._color)
		self._surface.fill(self._color)
		
		self._rect = self._surface.get_rect()
		self._rect.center = position

	def update(self,text):
		self._surface = RENDER_TEXT(text,self._font,self._color)

	def set_fill(self,color,text):
		self._color = color
		self._surface = RENDER_TEXT(text,self._font,self._color)


	def draw(self,SCREEN):
		SCREEN.blit(self._surface,self._rect)