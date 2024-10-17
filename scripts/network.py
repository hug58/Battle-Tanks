"""Server TCP connection"""

import socket
from typing import Tuple
from scripts.package import _unpack,_pack,BUFFER_SIZE

class Client:
    """ Client TCP connection """
    def __init__(self,addr:Tuple[str,int]):
        print(f"Connecting to {addr}")
        if addr is not None:
            self._socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self._socket.connect(addr)
            self._socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        else:
            self._socket = None
        self._data = {}

    def _send(self,player):
        try:
            player = _pack(player)
            self._socket.send(player)
            data_server = self._socket.recv(BUFFER_SIZE)
            data = _unpack(data_server)
            if data:
                self._data[data.num_player] = data
        except socket.error as error:
            print(error)
            self._socket.close()

    def _get_number_player(self):
        print("getting number")
        return _unpack(self._socket.recv(BUFFER_SIZE))
