"""Server TCP connection"""

import socket
from typing import Tuple
from scripts.commons.package import (Struct,
                                     BUFFER_SIZE_INIT_PLAYER,
                                     BUFFER_SIZE_EVENT,
                                     BUFFER_SIZE_PLAYER,
                                     OK_MESSAGE,
                                     JOIN_MESSAGE)

class Client:
    """ Client TCP connection """
    def __init__(self,addr:Tuple[str,int]):
        print(f"Connecting to {addr}")
        self._get_number_player = None
        self._data = {}

        if addr is not None:
            self._socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self._socket.connect(addr)
            self._socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            ok = self._socket.recv(BUFFER_SIZE_INIT_PLAYER)
            if ok == OK_MESSAGE:
                self._socket.send(JOIN_MESSAGE)
                self._get_number_player = Struct.unpack(self._socket.recv(BUFFER_SIZE_INIT_PLAYER))
                print(f"getting {self._get_number_player}")
                self._get_number_player = int(self._get_number_player)
        else:
            self._socket = None

    def send(self,player):
        try:
            player = Struct.pack(player)
            self._socket.send(player)
            data_server = self._socket.recv(BUFFER_SIZE_EVENT)
            data = Struct.unpack(data_server)
            if data:
                self._data[data.num_player] = data
        except socket.error as error:
            print(error)
            self._socket.close()

    def send_move(self, move:bytes):
        """ Send player moves"""
        try:
            self._socket.send(move)
            recv = self._socket.recv(BUFFER_SIZE_PLAYER)
            if recv != 'b':
                data_server = Struct.unpack_player(recv)


        except socket.error as e:
            self._socket.close()

    @property
    def get_number_player(self):
        """ get number of player """
        return self._get_number_player


