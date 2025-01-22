import pygame as pg 


class CameraComponent:
    """ The camera object that will be used to render the scene and interact """
    def __init__(self,width,height,screen_size):
        self.camera = pg.Rect((0,0),(width,height))
        self.width = width
        self.height = height
        self.screen_size = screen_size
    def apply(self,entity):
        """ Apply the camera transformation to the entity """
        return entity.rect.move(self.camera.topleft)
    def apply_rect(self,rect):
        """ mueve la posición de la surface a la pos de la camara en topleft (arriba/izquierda)"""
        return rect.move(self.camera.topleft)
    def update(self,target):
        """Targe en negativo para que en caso de llegar al extremo left (positivo), 
        el movimiento sea 0"""
        x_pos = -target.rect.centerx + self.screen_size[0] // 2
        y_pos = -target.rect.centery + self.screen_size[1] // 2
        #limit scrolling to map size
        x_pos = min(0,x_pos) #left
        y_pos = min(0,y_pos) #top
        x_pos = max(-(self.width - self.screen_size[0]),x_pos)
        y_pos = max(-(self.height - self.screen_size[1]),y_pos)
        self.camera = pg.Rect(x_pos,y_pos,self.width,self.height)

