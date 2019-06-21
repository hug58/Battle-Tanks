
import pygame as pg 
from script import image 

#Corta pero un poco dificil de leer
#Render_text =  lambda text: pg.font.Font('Pixel Digivolve.otf',30).render(text,2,pg.Color('#1CA4F4'))

def Render_text(text):
	font = pg.font.Font('Pixel Digivolve.otf',30)
	return font.render(text,2,pg.Color('#1CA4F4'))


class Life:
	def __init__(self,x,y,value):
		self.image = image['tank_{}'.format(value)]
		self.image_a = image['barra_{}'.format(value)]
		self.current_frames = 0
		self.frames = { 0:(0,0),
						1:(5,0),
						2:(10,0),
						3:(15,0),
						4:(20,0),
						5:(25,0),
							}
		self.current_image()

		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.clear = False


	def animation(self):
		self.current_image()
		self.current_frames +=1

		if self.current_frames == len(self.frames):
			self.clear = True

	def current_image(self):
		current = self.frames[self.current_frames]
		self.image = self.image_a.subsurface(current,(5,5))
		self.image = pg.transform.scale(self.image,(20,20))		


class Interface:
	def __init__(self,game):
		self.game = game
		self.image = pg.Surface((self.game.WIDTH,42))

		pos_x = [260,660]

		if self.game.player.value != 0:
			pos_x.reverse()

		self.player_lifes = self.lifes_pos(pos_x[0],self.game.player.value)
		self.player2_lifes = self.lifes_pos(pos_x[1],self.game.player_2.value)

		self.make_tablero(self.image)


	def lifes_pos(self,x,value):
		lifes_num = self.game.player.lifes_all
		life_list = [Life(x + 20*(i+1),10,value) for i in range(lifes_num)]
		return life_list

	def update(self,SCREEN):
		self.life_cont_player(self.game.player,self.player_lifes,self.game.player.value)
		self.life_cont_player(self.game.player_2,self.player2_lifes,self.game.player_2.value)
		
		self.draw(SCREEN)


	def life_cont_player(self,player,lifes,value):
			
			if len(lifes) > 0:
				if player.lifes_all < len(lifes) or player.lifes_all > len(lifes):
					if player.lifes_all < len(lifes):
						lifes[-1].animation()
						if lifes[-1].clear == True:
							lifes.pop()
					elif player.lifes_all > len(lifes):
						posx = lifes[-1].rect.x
						lifes.append(lifes(posx + 42 ,0,0))
					self.make_tablero(self.image)
			else:
				pass
				# value = value + 1


	def make_tablero(self,surface):
		self.image.fill((0,0,0))

		player1 = Render_text('Player 1')
		surface.blit(player1,(100,0))
		player2 = Render_text('Player 2')
		surface.blit(player2,(500,0))

		for vidas in self.player_lifes:
			surface.blit(vidas.image,vidas.rect)
		for vidas in self.player2_lifes:
			surface.blit(vidas.image,vidas.rect)

	def draw(self,SCREEN):
		SCREEN.blit(self.image,(0,self.game.HEIGHT))


if __name__ == '__main__':
	pass 
	