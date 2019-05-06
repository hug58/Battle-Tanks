
class Mission:
	def __init__(self,game):
		self.game = game
		self.objetivos = {"lvl_0": self.All_kill,}
		self.mission_actual = self.objetivos[self.game.lvl]

	def update(self):
		self.mission_actual()
		if self.mission_actual() == True:
			pass
			#print("¡Mission COMPLET!")

	def All_kill(self):
		if len(self.game.enemies) > 0:
			return False
		else:
			return True


if __name__ == '__main__':
    print("Este programa es independiente")
else:
    print("El modulo {name} ha sido importado".format(name = __name__))