import socket
#import pygame as pg
import threading as th
import struct
import json

#WIDTH = len(game.lvl_0[0])*SPACEMAP
#HEIGHT = len(game.lvl_0)*SPACEMAP
#SCREEN = pg.display.set_mode((WIDTH,HEIGHT))


class Client(th.Thread):
    def __init__(self):
        th.Thread.__init__(self)
        self.daemon = True
        self.data = {}

    def run(self):
        s = socket.socket()
        s.connect(("localhost",6000))
        exit = False

        while exit != True:
            
            len_str = s.recv(4)
            size = struct.unpack("!i",len_str)[0]
            #data = b""

            while size > 0:
                
                #if size >= 4096*3: 
                #    print(size)
                #    data = s.recv(4096*3)
                #else: data = s.recv(size)
                #if not data: break
                
                self.data = s.recv(size)
                self.data = json.loads(self.data)
                             
                #data = s.recv(size)
                #size -=len(data)
                #image_str += data
            
            #surface = pg.image.fromstring(image_str,(WIDTH,HEIGHT),"RGB")
            #SCREEN.blit(surface,(0,0))

            print(self.data)


#            for event in pg.event.get():
#               if event.type == pg.QUIT: exit = True

            #pg.display.flip()


if __name__ == "__main__":
    Client().run()
    #game = multiplayer.Load_game(game.lvl_map)
    #game.run()

    pg.quit()
