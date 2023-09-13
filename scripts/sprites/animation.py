
class Animation:
    """it Animate with sprites files"""
    def __init__(self,image,frames):
        self._frames = frames
        self._current_frame = 0
        self._image = image
        self._delay = 4
        self._cont = 0
        self._done = False
        self.image = None

    def _update(self):
        self.image = self._image.subsurface(self._frames[self._current_frame])
        self._cont +=1
        	
        if self._cont == self._delay:
            self._current_frame +=1
            self._cont = 0
        if self._current_frame == len(self._frames):
            self._done =True

