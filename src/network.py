"""Server TCP connection"""

import socket
import sys
from typing import Tuple
from src.commons.package import (Struct,
                                     BUFFER_SIZE_INIT_PLAYER,
                                     )

class NetworkComponent:
    """ Client TCP connection """
    def __init__(self,addr:Tuple[str,int], name:str="John"):
        print(f"Connecting to {addr}, Player: {name}")
        self.data_udp:dict = {}
        self.name = name
        self.addr = addr

        self._socket_tcp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self._socket_tcp.connect(addr)
        self._socket_tcp.setsockopt(socket.SOL_SOCKET,socket.TCP_NODELAY,1)
        self._player_data:dict = self.load_data()

        self._socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._addr_udp = ('localhost', 12345)


    def load_data(self) -> dict:
        """ Load player data init"""
        ok = self._socket_tcp.recv(Struct.BUFFER_SIZE_EVENT)
        if ok == Struct.OK_MESSAGE:
            self._socket_tcp.send(Struct.pack(self.name))
            join = self._socket_tcp.recv(Struct.BUFFER_SIZE_EVENT)
            if  join == Struct.USER_NOT_AVAILABLE:
                print("USER NO AVAILABLE")
                sys.exit(1)

            data = self._socket_tcp.recv(14)
            data = Struct.unpack_player(data)
            return {
                    "position": data[1],
                    "x": data[2],
                    "y": data[3],
                    "cannon_x": data[4],
                    "cannon_y": data[5],
                    "angle": data[6],
                    "angle_cannon": data[7]
            }

    def recv_move_player(self) :
        """ get data player """
        try:

            self._socket_tcp.setblocking(False)
            data = self._socket_tcp.recv(300)
            # self._socket_tcp.setblocking(True)
            modify_data = lambda player_arr: {
                                "status": player_arr[0],
                                "position": player_arr[1],
                                "x": player_arr[2],
                                "y": player_arr[3],
                                "cannon_x": player_arr[4],
                                "cannon_y": player_arr[5],
                                "angle": player_arr[6],
                                "angle_cannon": player_arr[7]
                            }


            if data != b'':
                players = list(map(modify_data, Struct.unpack_players(data)))
                return players

        except (BlockingIOError, socket.error) as e:
            # print(f"THERE IS A ERROR: {e}")
            pass

        return {
        }

    def send_move_tcp(self, move:bytes):
        try:
            self._socket_tcp.send(move)
        except socket.error as e:
            self._socket_tcp.close()

    def send_move(self, move:bytes):
        """ Send player moves"""
        try:
            data = {
                "move": move,
                "position": self.player_number
            }
            self._socket_udp.sendto(Struct.pack(data),self._addr_udp)
            data, server = self._socket_udp.recvfrom(14)
            data_player = Struct.unpack_player(data)

            if (data_player[0] == Struct.UPDATE_PLAYER or
                    data_player[0] == Struct.NEW_PLAYER):
                self.data_udp[data_player[1]] = {
                    "status": data_player[0],
                    "position": data_player[1],
                    "x": data_player[2],
                    "y": data_player[3],
                    "cannon_x": data_player[4],
                    "cannon_y": data_player[5],
                    "angle": data_player[6],
                    "angle_cannon": data_player[7]
                }

        except socket.error as e:
            self._socket_udp.close()

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

