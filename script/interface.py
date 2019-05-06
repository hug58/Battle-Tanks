from script import *  

Render_text =  lambda text: pg.font.Font("Pixel Digivolve.otf",30).render(text,2,pg.Color("#1CA4F4"))

class Life:
	def __init__(self,x,y,value):
		self.image = image["tank_{value}".format(value = value )]
		self.image = self.image.subsurface((0,20),(20,20))
		self.x = x
		self.y = y

class Interface:
	def __init__(self,game):
		self.game = game
		self.image = pg.Surface((self.game.WIDTH,42))

		self.vidas_player_1 = [ Life(120 + 40*(i+1),10,0) for i in range(3)]
		self.vidas_player_2 = [Life(632 + 42*(i+1),10,1) for i in range(3)] if len(self.game.sprites) > 1 else []
		self.make_tablero(self.image)

	def update(self):
		for sprites in self.game.sprites:
			if sprites.value == 0:
				if len(self.vidas_player_1) > 0:
					if sprites.vidas < len(self.vidas_player_1) or sprites.vidas > len(self.vidas_player_1):
						if sprites.vidas < len(self.vidas_player_1):
							self.vidas_player_1.pop()
						elif sprites.vidas > len(self.vidas_player_1):
							posx = self.vidas_player_1[-1].x
							self.vidas_player_1.append(Life(posx + 42 ,0,0))

						self.make_tablero(self.image)

				else:

					value = sprites.value + 1
					cadena = "Jugador {value} Perdió!".format(value = value)

					print(cadena) if len(self.game.sprites) > 1 else print("GAME OVER")
					print(cadena) if len(self.game.sprites) > 1 else print("GAME OVER")

			if sprites.value == 1:
				if len(self.vidas_player_2) > 0:
					if sprites.vidas < len(self.vidas_player_2) or sprites.vidas > len(self.vidas_player_2):
						if sprites.vidas < len(self.vidas_player_2):
							self.vidas_player_2.pop()
						elif sprites.vidas > len(self.vidas_player_2):
							posx = self.vidas_player_2[-1].x
							self.vidas_player_2.append(Life(posx + 42 ,0,1))
						self.make_tablero(self.image)
				else:

					value = sprites.value + 1
					cadena = "Jugador {value} Perdió!".format(value = value)

					print(cadena)

	def make_tablero(self,surface):

		#self.image.fill(pg.Color("#04441C"))
		self.image.fill((0,0,0))

		player1 = Render_text("Player 1")
		surface.blit(player1,(0,0))
		if len(self.vidas_player_2) > 0:
			player2 = Render_text("Player 2")
			surface.blit(player2,(500,0))


		for vidas in self.vidas_player_1:
			surface.blit(vidas.image,(vidas.x,vidas.y))
		for vidas in self.vidas_player_2:
			surface.blit(vidas.image,(vidas.x,vidas.y))

	def draw(self,SCREEN):
		SCREEN.blit(self.image,(0,self.game.HEIGHT))


if __name__ == '__main__':
    print("Este programa es independiente")
else:
    print("El modulo {name} ha sido importado".format(name = __name__))