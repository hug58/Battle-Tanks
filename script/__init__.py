import pygame as pg
import os.path,sys

pg.display.init()
pg.font.init()



# resolve_route = lambda relative,route: os.path.join(os.path.abspath(relative),route)

def resolve_route(rute,relative = '.'):
	if hasattr(sys,'_MEIPASS'):
		return os.path.join(sys._MEIPASS,rute)

	return os.path.join(os.path.abspath(relative),rute)

pg.mixer.init()

import math
image = {	
			'tank_0': pg.image.load(resolve_route('image/limonero_tank.png')),
			'tank_0_gun': pg.image.load(resolve_route('image/limonero_gun.png')),			
			'tank_1': pg.image.load(resolve_route('image/uvadero_tank.png')),
			'bullet_1': pg.image.load(resolve_route('image/bullet_a.png')),
			'bullet_0': pg.image.load(resolve_route('image/bullet_lvl2.png')),
			'tiles': pg.image.load(resolve_route('image/tiles.png')),
			'gun': pg.image.load(resolve_route('image/gun2x.png')),
			'wave_shot' : pg.image.load('image/effect_shot.png'),
			'explosion': pg.image.load('image/effect_explosion.png'),
			'barra_0': pg.image.load('image/salud_barra.png'),
			'barra_1': pg.image.load('image/salud_barra_2.png'),
			'dead_0': pg.image.load('image/limonero_tank_explosion.png'),
			'dead_1': pg.image.load('image/uvadero_tank_explosion.png'),
}

sound = { 
			'shot': pg.mixer.Sound(resolve_route('sound/shot.wav')),	
			'box': pg.mixer.Sound(resolve_route('sound/box.wav')),
			'boomsnd': pg.mixer.Sound(resolve_route('sound/boomsnd.wav')),
			}


if __name__ == '__main__':
	pass 
