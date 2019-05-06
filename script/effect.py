from script import * 

class Animation:
	
	def __init__(self,frames):
		self.current_frames = 0
		self.limit = len(frames)
		self.step = 15
		self.cont = 0
		
	def update(self,condition):
		
		if self.cont >= self.step:			
			if self.current_frames < self.limit: self.current_frames +=1
			if self.current_frames == self.limit:
				self.current_frames = 0 if condition == 1 else self.current_frames
				
			self.cont = 0
		elif self.cont == 0:
			self.current_frames = 0

		self.cont +=1

class Effect(pg.sprite.Sprite):
	def __init__(self,pos,angle,frames,size,image):

		pg.sprite.Sprite.__init__(self)
		self.effect = image
		self.size = size

		self.image = self.effect.subsurface((0,0),self.size)
		self.image = pg.transform.scale(self.image,(self.size[0]*2,self.size[1]*2))
		self.rect = self.image.get_rect()

		self.radians = math.radians(angle)		
		self.rect.x = (pos[0] - (20 * math.sin(self.radians))) - self.rect.width//2 
		self.rect.y = pos[1] - (20 * math.cos(self.radians)) - self.rect.height //2
		
		self.pos = pos
		self.frames = frames

		self.animation = Animation(self.frames)
		self.animation.step = 2
		self.pos = pos

	def update(self):

		frame = self.animation.current_frames
		self.animation.update(0)
		self.image = self.effect.subsurface(self.frames[frame],self.size)
		self.image = pg.transform.scale(self.image,(self.size[0]*2,self.size[1]*2))

		if self.animation.current_frames >= len(self.frames): self.kill()

		self.rect.x = self.pos[0] - (30 * math.sin(self.radians)) - self.rect.width//2 
		self.rect.y = self.pos[1] - (35 * math.cos(self.radians)) - self.rect.height //2



if __name__ == '__main__':
    print("Este programa es independiente")
else:
    print("El modulo {name} ha sido importado".format(name = __name__))