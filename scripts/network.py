"""Server TCP connection"""

import socket
import sys
from typing import Tuple
from scripts.commons.package import (Struct,
                                     BUFFER_SIZE_INIT_PLAYER,
                                     )

class Client:
    """ Client TCP connection """
    def __init__(self,addr:Tuple[str,int], name:str="John"):
        print(f"Connecting to {addr}, Player: {name}")
        self._player_data:dict = {}
        self._data:dict = {}
        self.name = name
        self.addr = addr

        if addr is not None:
            self._socket_tcp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self._socket_tcp.connect(addr)
            self._socket_tcp.setsockopt(socket.SOL_SOCKET,socket.TCP_NODELAY,1)

            ok = self._socket_tcp.recv(Struct.BUFFER_SIZE_EVENT)
            if ok == Struct.OK_MESSAGE:
                self._socket_tcp.send(Struct.pack(self.name))
                join = self._socket_tcp.recv(Struct.BUFFER_SIZE_EVENT)
                if  join == Struct.USER_NOT_AVAILABLE:
                    print("USER NO AVAILABLE")
                    sys.exit(1)

                print("PROCESS START")
                data = self._socket_tcp.recv(14)
                print(f"LO LLEGADO: {data}")
                data = Struct.unpack_player(data)
                print("PROCESS END")
                self._player_data = {
                    "position": data[1],
                    "x": data[2],
                    "y": data[3],
                    "cannon_x": data[4],
                    "cannon_y": data[5],
                    "angle": data[6],
                    "angle_cannon": data[7]
                }

        else:
            self._socket = None


    def recv_move_player(self) -> dict:
        """ get data player """
        try:
            self._socket_tcp.setblocking(False)
            data = self._socket_tcp.recv(14)
            # self._socket_tcp.setblocking(True)

            if data != b'':
                data = Struct.unpack_player(data)
                if (data[0] == Struct.UPDATE_PLAYER or
                        data[0] == Struct.NEW_PLAYER):
                    return {
                        "status": data[0],
                        "position": data[1],
                        "x": data[2],
                        "y": data[3],
                        "cannon_x": data[4],
                        "cannon_y": data[5],
                        "angle": data[6],
                        "angle_cannon": data[7]
                    }
        except BlockingIOError:
            pass
            # print("No hay datos disponibles para recibir en este momento.")

        return {
        }


    def send_move(self, move:bytes):
        """ Send player moves"""
        try:
            self._socket_tcp.send(move)
        except socket.error as e:
            self._socket_tcp.close()


    @property
    def player_data(self):
        """ get number of player """
        return self._player_data

    @property
    def player_number(self):
        """ get number of player """
        return self._player_data["position"] if self._player_data != {} else 0

    @property
    def socket_tcp(self):
        self._socket_tcp.send(Struct.CLOSE_CONN)
        return self._socket_tcp

