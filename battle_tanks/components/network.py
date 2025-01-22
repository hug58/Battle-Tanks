"""Server TCP connection"""

import socket
from typing import Tuple, List, Union
from battle_tanks.commons.package import Struct

from queue import SimpleQueue

class NetworkComponent:
    """ Client TCP connection """

    SEND_Q = SimpleQueue()
    UPDATE_Q = SimpleQueue()


    def __init__(self, addr: Tuple[str, int], name: str = "John"):
        print(f"Connecting to {addr}, Player: {name}")
        self.name = name
        self.addr = addr
        self.lvl_map: str = ""

        self._socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket_tcp.connect(addr)
        self._socket_tcp.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1)

        self.game_state: bytes = b""
        self._player_data: Union[dict, bytes] = self.load_data()


    def load_data(self) -> Union[dict, bytes]:
        """ Load player data INIT """
        ok = self._socket_tcp.recv(Struct.BUFFER_SIZE_EVENT)
        if ok == Struct.OK_MESSAGE:
            self._socket_tcp.send(Struct.pack(self.name))
            lvl_map = self._socket_tcp.recv(Struct.BUFFER_SIZE_LVL_MAP)
            if lvl_map == Struct.USER_NOT_AVAILABLE:
                return Struct.USER_NOT_AVAILABLE

            self.lvl_map = Struct.unpack(lvl_map)

            data = self._socket_tcp.recv(Struct.SIZE_PLAYER)
            data_player = Struct.unpack_player(data)
            size_map = Struct.unpack_single_data(self._socket_tcp.recv(Struct.BUFFER_SIZE_EVENT))

            for i in range(size_map[0]):
                split_map = self._socket_tcp.recv(Struct.BUFFER_SPLIT_MAP)
                self.game_state += split_map

            return {
                "position": data_player[1],
                "x": data_player[2],
                "y": data_player[3],
                "angle": data_player[4],
                "angle_cannon": data_player[5]
            }

    @staticmethod
    def _modify_data(data_arr: list) -> dict:
        """
        MODIFY PLAYER AND EVENTS
        """

        if data_arr[0] in Struct.STATUS_PLAYER:
            return {
                "status": data_arr[0],
                "position": data_arr[1],
                "x": data_arr[2],
                "y": data_arr[3],
                "angle": data_arr[4],
                "angle_cannon": data_arr[5],
                "damage_indicator": data_arr[6]
            }

        elif data_arr[0] == Struct.BROKE_BRICK:
            return {
                "status": data_arr[0],
                "x": data_arr[1],
                "y": data_arr[2],
                "w": data_arr[3],
                "h": data_arr[4],
            }


    def recv_move_player(self) -> List[dict]:
        """ get data player and states game"""
        try:
            data = self._socket_tcp.recv(120)
            if data != b'':
                data_set = Struct.unpack_all_data(data)
                return list(map(NetworkComponent._modify_data, data_set))
        except BlockingIOError as e:
            # print(f"BLOCKING AS: {e}")
            pass
        except socket.error as e:
            print(f"THERE IS A ERROR: {e}")
            pass

        return []


    def send_move_tcp(self, move: bytes):
        try:
            self._socket_tcp.send(move)
        except socket.error as e:
            self._socket_tcp.close()


    @property
    def player_data(self) -> Union[dict, bytes]:
        """ get number of player """
        return self._player_data


    @property
    def player_number(self) -> int:
        """ get number of player """
        if self._player_data == Struct.USER_NOT_AVAILABLE:
            return 0

        return self._player_data["position"]


    @property
    def socket_tcp(self) -> socket.socket:
        return self._socket_tcp


    @staticmethod
    def check_name(addr: tuple, name: str) -> Union[bool, socket.error]:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            sock.connect(addr)

            if sock.recv(Struct.BUFFER_SIZE_EVENT) == Struct.OK_MESSAGE:
                sock.send(Struct.pack(name + "-c"))
                return sock.recv(1) == Struct.OK_MESSAGE

        except socket.error as e:
            return e

        return False


    def get_events_to_game_state(self):
        """
        Extracts and returns the events from the current game state.

        This method uses the Struct class to unpack events from the 
        game_state attribute of the instance.

        Returns:
            list: A list of events extracted from the game state.
        """
        return Struct.unpack_events(self.game_state)


    @classmethod
    def send_keys(cls, keys: List[bytes]) -> None:
        for action in keys:
            cls.SEND_Q.put(action)

    
    @classmethod
    def recv_to_queue(cls) -> bytes:
        data = []
        while cls.UPDATE_Q.empty() is False:
            data.extend(cls.UPDATE_Q.get())
    
        return data