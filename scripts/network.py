
import threading as th 
import socket
import pygame as pg


'''
Locals
'''
from scripts.package import _unpack,_pack,BUFFER_SIZE
from scripts.player import Player



class Client:

	def __init__(self,addr):

		self._socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self._socket.connect(addr)

		#Desbloquea el puerto
		self._socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		self._data = {}


	def _send(self,player):

		try:
			player = _pack(player)
			self._socket.send(player)

			data_server = self._socket.recv(BUFFER_SIZE)
			data = _unpack(data_server)

			if data:
				self._data[data._num_player] = data
			
		except socket.error as e:
			print(e)
			print("Conexión perdida con el servidor.")
			self._socket.close()


	def _get_number_player(self):
		return _unpack(self._socket.recv(BUFFER_SIZE))



if __name__ == '__main__':
	addr = ('localhost',6000)
	c = Client(addr)

