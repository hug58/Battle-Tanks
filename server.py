import socket
import pygame as pg
import threading as th
import struct


WIDTH = 400
HEIGHT = 300

#SCREEN = pg.display.set_mode((WIDTH,HEIGHT))

class Server(th.Thread):
	def __init__(self,surface):
		th.Thread.__init__(self)
		self.surface = surface
		self.daemon = True

	def run(self):

		s = socket.socket()
		s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		s.bind(("localhost",6000))
		s.listen(1)
		print("Esperando conexión...")	

		try:

			conn,addr = s.accept()
			print(f"Conexión establecida con {addr}")


			while True:
				image_str = pg.image.tostring(self.surface,"RGB")
				len_str = struct.pack("!i",len(image_str))
				conn.send(len_str)
				conn.send(image_str)

		except Exception as e: print(e)

		finally:
			print("Cerrando socket...")
			conn.close()
			s.close()
			pg.quit()


