"""Server TCP connection"""

import socket
import sys
from typing import Tuple, List, Union
from src.commons.package import Struct

class NetworkComponent:
    """ Client TCP connection """

    def __init__(self,addr:Tuple[str,int], name:str="John"):
        print(f"Connecting to {addr}, Player: {name}")
        self.name = name
        self.addr = addr

        self._socket_tcp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self._socket_tcp.connect(addr)
        self._socket_tcp.setsockopt(socket.SOL_SOCKET,socket.TCP_NODELAY,1)
        self._player_data:Union[dict,bytes] = self.load_data()


    def load_data(self) -> Union[dict, bytes]:
        """ Load player data init"""
        ok = self._socket_tcp.recv(Struct.BUFFER_SIZE_EVENT)
        if ok == Struct.OK_MESSAGE:
            self._socket_tcp.send(Struct.pack(self.name))
            join = self._socket_tcp.recv(Struct.BUFFER_SIZE_EVENT)
            if  join == Struct.USER_NOT_AVAILABLE:
                return Struct.USER_NOT_AVAILABLE

            data = self._socket_tcp.recv(14)
            data = Struct.unpack_player(data)
            return {
                    "position": data[1],
                    "x": data[2],
                    "y": data[3],
                    "angle": data[4],
                    "angle_cannon": data[5]
            }


    def recv_move_player(self) -> List[dict]:
        """ get data player """
        try:
            self._socket_tcp.setblocking(False)
            data = self._socket_tcp.recv(Struct.BUFFER_SIZE_PLAYER)
            self._socket_tcp.setblocking(True)
            modify_data = lambda player_arr: {
                                "status": player_arr[0],
                                "position": player_arr[1],
                                "x": player_arr[2],
                                "y": player_arr[3],
                                "angle": player_arr[4],
                                "angle_cannon": player_arr[5]
                            }

            if data != b'':
                players = list(map(modify_data, Struct.unpack_players(data)))
                return players

        except (BlockingIOError, socket.error) as e:
            # print(f"THERE IS A ERROR: {e}")
            pass

        return []


    def send_move_tcp(self, move:bytes):
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
        if self._player_data == Struct.USER_NOT_AVAILABLE:
            return 0

        return self._player_data["position"]


    @property
    def socket_tcp(self):
        self._socket_tcp.send(Struct.CLOSE_CONN)
        return self._socket_tcp

