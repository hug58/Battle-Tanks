
import socket
import threading as th
import time
import sys
import os
import queue
import select
import logging
import random
from typing import Union, Dict, List, Optional
from .conexions import DatabaseManager
from scripts.commons.package import (Struct,
                                     BUFFER_SIZE_EVENT)

q = queue.Queue()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
lock = th.Lock()
TICK_INTERVAL = 0.05  # 50 ms por tick (20 ticks/segundo)
POSITIONS = {
    0:[323,677],
    1:[404, 161]
}

def generate_random_numbers_from_time(n=5):
    random.seed(int(time.time()))
    random_numbers = [random.randint(0, 9) for _ in range(n)]
    return ''.join(map(str, random_numbers))


class Server:
    """Server made in socket TCP"""

    def __init__(self,addr):
        self._data:Dict[int,dict] = {}
        self._filter_name:list = []
        self._current_player = 0
        self._socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self._socket.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1)
        self._socket.bind(addr)
        self._max_players = 10
        self._socket.listen(self._max_players)
        self.sockets = []

        DatabaseManager.configure({"database_name":"database.json"})

        self.persistence = DatabaseManager.get()
        self.room = str(generate_random_numbers_from_time())

        print(f"ROOM: {self.room}")

        th_1 = th.Thread(target = self._conexions, daemon = True)
        th_2 = th.Thread(target = self._receive, daemon = True)

        th_1.start()
        th_2.start()

        while True:
            try:
                op = input("\n>")
                if op == "users":
                    for _,player in self._data.items():
                        print(player.get("name"))
                elif op == "data":
                    for data in self._data.items():
                        print(data)
                elif op == "exit":
                    self._socket.close()
                    sys.exit(1)
                elif op in ("help","h"):
                    print("OPTIONS: users and data")
            except KeyboardInterrupt:
                self._socket.close()
                os.remove("database.json")
                sys.exit(1)

    def _conexions(self):
        logger.warning("Waiting conexions...")

        while True:
            try:
                if len(self._data) >= self._max_players:
                    time.sleep(3)
                    continue

                conn,addr = self._socket.accept()
                conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                conn.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536)
                conn.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)

                conn.send(Struct.OK_MESSAGE)
                data = conn.recv(Struct.BUFFER_SIZE_NAME)

                try:
                    if data != b'':
                        data = Struct.unpack(data)

                        print(f"NOMBRE: {data}")

                        current = list(set(range(self._max_players)) - set([position for position, _ in self._data.items()]))[0]
                        searching_player = self.persistence.find("player", {"name": data})

                        if len(searching_player) > 0:
                            """check user if exists in self._data"""
                            if data in self._filter_name:
                                conn.send(Struct.USER_NOT_AVAILABLE)
                                continue

                        conn.send(Struct.JOIN_MESSAGE)

                        if len(searching_player) == 0:
                            player = self.persistence.save(
                                "player",{
                                    # "status": "on",
                                    # "room_id":self.room,
                                    "name": data,
                                    "position": current,
                                    # "addr": addr,
                                    "x": 323,
                                    "y": 677,
                                    "cannon_x":338,
                                    "cannon_y":692,
                                    "angle":0,
                                    "angle_cannon":0
                                })
                        else:
                            player = searching_player[0]
                            player["addr"] = addr

                        self._filter_name.append(player.get("name"))
                        player["conn"] = conn

                        """Current Player in Queue."""
                        q.put(player)
                        self._current_player +=1

                except EOFError as e:
                    logger.error(f"ERROR[{e}] CLIENT: {addr}" )
            except BlockingIOError as e:
                logger.error(f"ERROR[{e}] BlockingIOError")

    def _receive(self):
        while True:
            # start_time = time.time()

            if  len(self._data) > 0:
                readable, _, _ = select.select(self.sockets, [], [], 0)
                available: List[socket.socket] = readable
                for sock in available:
                    try:
                        data = sock.recv(BUFFER_SIZE_EVENT)
                        if data != b'':
                            position = self._get_player_position(sock)
                            if position >= 0:
                                self._messages_client(data, position)

                    except ConnectionRefusedError as e:
                        logger.error(f"LOG ERROR: {e}")
                        for position, player in self._data.items():
                            if sock == player.get("conn"):
                                player["deleted"] = True
                                q.put(player)

                        self.sockets.remove(sock)


            # elapsed_time = time.time() - start_time
            # max_time = max(0, TICK_INTERVAL - elapsed_time)
            # time.sleep(max_time)

            if not q.empty():

                new_player:dict = q.get()
                current = new_player.get("position")

                if new_player.get("deleted"):
                    del self._data[current]
                    self._filter_name.remove(new_player.get("name"))
                    continue

                others_players:Dict[int,dict] = self._data.copy()
                self._data[current] = new_player

                encoded_message = Struct.pack_player(None, new_player)
                conn_new_player:socket.socket = new_player.get("conn")
                conn_new_player.send(encoded_message)

                if len(others_players) > 0:
                    for position,player in others_players.items():
                        conn: socket.socket = player.get("conn")
                        encoded_message = Struct.pack_player(None, new_player, Struct.NEW_PLAYER)
                        conn.send(encoded_message)

                    for position,player in others_players.items():
                        encoded_message = Struct.pack_player(None, player, Struct.OLD_PLAYER)
                        conn_new_player.send(encoded_message)

                self.sockets: List[socket.socket] = [player["conn"] for _, player in self._data.items()]

    def _messages_client(self,data:Union[bytes,None], player_number:int) -> None:
        """ :param data: events player[const bytes] or add new player
            :param player_number: player position in self._data
        """

        #TODO: check the kinds of options
        player_data:dict = self._data[player_number]
        encoded_message = Struct.pack_player(data, player_data)


        for position, player in self._data.items():
            conn:socket.socket = player.get("conn")
            conn.send(encoded_message)

    def _get_player_position(self, conn) -> int:
        for position, player in self._data.items():
            if player.get("conn") == conn:
                return position
        return -1



if __name__ == '__main__':
    ip_bind = os.getenv("IP_BIND","0.0.0.0")
    port = os.getenv("SERVER_PORT",8500)

    print('IP THE SERVER: {ip}'.format(ip = ip_bind))
    print('PORT : {port}'.format(port = port))
    Server((ip_bind,port))
