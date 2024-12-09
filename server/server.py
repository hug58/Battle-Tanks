
import socket
import threading as th
import time
import sys
import os
import queue
import logging
import random
from typing import  Union,Dict
from .conexions import DatabaseManager
from scripts.commons.package import (Struct,
                                     BUFFER_SIZE_NAME,
                                     BUFFER_SIZE_EVENT)

q = queue.Queue()
logger = logging.getLogger()
# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)


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
        self._socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self._socket.bind(addr)
        self._max_players = 10
        self._socket.listen(self._max_players)

        # DatabaseManager.configure({"database_name":"mongo",
        #                            "db":"testing",
        #                            "host":"localhost",
        #                            "port":27017})

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
                break

    def _conexions(self):
        logger.warning("Waiting conexions...")

        while True:
            try:
                if len(self._data) >= self._max_players:
                    time.sleep(3)
                    continue

                conn,addr = self._socket.accept()
                conn.send(Struct.OK_MESSAGE)
                data = Struct.unpack(conn.recv(BUFFER_SIZE_NAME))

                try:
                    if data != b'':
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
                                })
                        else:
                            player = searching_player[0]
                            player["addr"] = addr


                        self._filter_name.append(player.get("name"))

                        player["conn"] = conn
                        self._data[current] = player
                        """Current Player in Queue"""
                        q.put(current)
                        self._current_player +=1

                except EOFError as e:
                    logger.error(f"ERROR[{e}] CLIENT: {addr}" )
            except BlockingIOError as e:
                logger.error(f"ERROR[{e}] BlockingIOError")

    def _receive(self):
        while True:
            if len(self._data) > 0 and q.empty():
                for position,player in self._data.items():
                    try:
                        conn = player.get("conn")
                        data:bytes = conn.recv(BUFFER_SIZE_EVENT)
                        if data != b'':
                            self._messages_client(data,position)
                    except ConnectionResetError as e:
                        logger.warning(f"ConnectionResetError: [{e}]")
                        self._data.pop(position)
                    except BlockingIOError as e:
                        logger.warning(f"BlockingIOError: [{e}]")
                        self._data.pop(position)
                    except EOFError as e:
                        logger.warning(f"EOFError: [{e}]")
                        self._data.pop(position)
                    except ConnectionAbortedError as e:
                        logger.warning(f"ConnectionAbortedError: [{e}]")
                        self._data.pop(position)
                    except BrokenPipeError as e:
                        logger.warning(f"BrokenPipeError: [{e}]")
                        self._data.pop(position)

            elif not q.empty():
                current:int = q.get()

                if current not in self._data:
                    logger.warning("[LOG] current disconnect")
                    continue

                new_player:dict = self._data[current]
                self._data.pop(current)
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



if __name__ == '__main__':
    ip_bind = os.getenv("IP_BIND","0.0.0.0")
    port = os.getenv("SERVER_PORT",8500)

    print('IP THE SERVER: {ip}'.format(ip = ip_bind))
    print('PORT : {port}'.format(port = port))
    Server((ip_bind,port))
