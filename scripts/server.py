
import socket
import sys
import threading as th 
import pygame as pg 


#Locals
from scripts.player import Player
from scripts.package import _unpack,_pack,BUFFER_SIZE


class Server:
	'''docstring for Server'''
	def __init__(self,addr):

		self._clients = []
		self._data = {}


		self._current_player = 0


		self._socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self._socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

		self._socket.bind(addr)
		self._socket.listen(10)
		self._socket.setblocking(False)

		hilo_1 = th.Thread(target = self._conexions,daemon = True)
		hilo_1.start()

		hilo_2 = th.Thread(target = self._recevie,daemon = True)
		hilo_2.start()

		while 1:

			data = input('\n>')
			if data == 'exit':
				self._socket.close()
				sys.exit()
				break
			elif data == 'users':
				for i,addr in self._clients:
					print(addr[0])

			elif data == 'data':
				for i in self._data.keys():
					print(self._data[i])

	def _conexions(self):

		print('Esperando conexiones ...')
		while 1:
			try:
				if len(self._clients) < 10:
					conn,addr = self._socket.accept()
					conn.setblocking(False)
					print(f'Connect with {addr}')
					"""
					Number player
					"""
					conn.send(_pack(self._current_player))
					client = (conn,[addr,self._current_player])

					self._current_player +=1
					if self._current_player == 4:
						self._current_player = 0

					self._clients.append(client)
					print(f'Numero de conexiones: {len(self._clients)}' )
				else:
					break
			except:
				pass


	def _recevie(self):
		while 1:
			if len(self._clients) > 0:
				for conn,addr in self._clients:
					try:
						data = conn.recv(BUFFER_SIZE)
						if data:
							data = _unpack(data)
							data._num_player = addr[1]
							self._data[data._num_player] = data
							self._messages_client(data,conn)

						else:
							'''
							Por el momento solo elimina el cliente cuando terminan todos, hay que repararlo.
							'''
							print(f'Ya no recibo datos de {addr[0]}')
							print("Eliminando cliente...")
							#conn.close()
							
							#Eliminando jugador...
							self._data.pop(addr[1])
							self._clients.remove((conn,addr))
							print(f'Numero de conexiones: {len(self._clients)}' )
					except:
						pass
						

	def _messages_client(self,data,client):
		data_pack = _pack(data)				
		for conn,addr in self._clients:
			try:
				if conn != client:
					conn.send(data_pack)
			except:
				if client in self._clients:
					self._clients.remove(client)




if __name__ == '__main__':
	addr = ('localhost',6000)
	s = Server(addr)


