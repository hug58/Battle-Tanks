
import socket
import threading as th
import time
import sys
import os
import queue
import logging
import random
from typing import Dict,Tuple
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
from .conexions import DatabaseManager
from src.commons.package import (Struct,BUFFER_SIZE_EVENT)

q = queue.SimpleQueue()

if os.path.exists("battle_server.log"):
    os.remove("battle_server.log")

logging.basicConfig(filename="battle_server.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logging.info("Running Battle Tanks")
logger = logging.getLogger('BattleTanks')

lock = th.Lock()
TICK_RATE = 1 / 20  # 5 times per second
POSITIONS = {
    0:[323,677],
    1:[404, 161]
}

def generate_random_numbers_from_time(n=5):
    random.seed(int(time.time()))
    random_numbers = [random.randint(0, 9) for _ in range(n)]
    return ''.join(map(str, random_numbers))


def send_data(conn:socket.socket, data:bytes):
    try:
        logger.debug(f"SEND DATA SUCCESS: {data}. TO: {th.current_thread().name}")
        conn.send(data)
    except (TimeoutError,ConnectionResetError,BrokenPipeError) as e:
        logger.error(f"SEND DATA FAILED: {data}. TO: {th.current_thread().name}. EXCEPT: {e}")

class Server:
    """Server made in socket TCP"""

    def __init__(self,addr):
        self.tick_last_sent = time.time()
        self._data:Dict[int,dict] = defaultdict(dict)
        self._sockets = []

        self._filter_name:list = []
        self._current_player = 0

        self._socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self._socket.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
        self._socket.bind(addr)

        self._max_players = Struct.MAX_PLAYERS
        self.executor = ThreadPoolExecutor(max_workers=10,thread_name_prefix="CLIENT_RECV")
        self._socket.listen(self._max_players)

        DatabaseManager.configure({"database_name":"database.json"})
        self.persistence = DatabaseManager.get()

        th_1 = th.Thread(target = self._conexions, daemon = True)
        th_1.start()

        th_2 = th.Thread(target=self.handle_menu, daemon = True)
        th_2.start()

        self._receive()

    def handle_menu(self):
        logger.debug(f"INIT HANDLE_MENU {th.current_thread().name}")
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
                    os.remove("database.json")
                    sys.exit(1)
                elif op in ("help","h"):
                    print("OPTIONS: users and data")
            except KeyboardInterrupt as e:
                self._socket.close()
                os.remove("database.json")
                sys.exit(1)

    def handle_client(self,client_socket: socket.socket):
        logger.warning(f"RUNNING NEW THREAD CLIENT: {client_socket.getsockname()} - THREAD -- {th.current_thread().name}")
        while True:
            try:
                data = client_socket.recv(Struct.BUFFER_SIZE_EVENT)
                if not data:
                    position = self._get_player_position(client_socket)
                    if position == -1:
                        break

                    player = self._data[position]
                    player["deleted"] = True
                    q.put(player)

                if data == Struct.CLOSE_CONN:
                    logger.warning(f"CLOSED: {client_socket.getsockname()} "
                                   f"THREAD -- {th.current_thread().name}")

                    for position, player in self._data.items():
                        if client_socket == player.get("conn"):
                            player["deleted"] = True
                            q.put(player)

                position = self._get_player_position(client_socket)
                if position >= 0:
                    player_data: dict = self._data[position]
                    encoded_message = Struct.pack_player(data, player_data)

                    # self.persistence.update(
                    #     collection="players",
                    #     query={"name": player_data.get("name")},
                    #     new_data=player_data)

                    q.put(encoded_message)

            except (ConnectionResetError, ConnectionRefusedError) as e:
                logger.error(f"LOG ERROR: {e}")
                for position, player in self._data.items():
                    if client_socket == player.get("conn"):
                        player["deleted"] = True
                        q.put(player)
                break

        client_socket.close()

    def _conexions(self):
        logger.warning(f"WAITING CONEXIONS --- {th.current_thread().name}")
        while True:
            try:
                if len(self._data) >= self._max_players:
                    time.sleep(10)
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
                        logger.warning(f"ADD NEW_CONEXIONS: {data}")

                        current = list(set(range(self._max_players)) - set([position for position, _ in self._data.items()]))[0]
                        searching_player = self.persistence.find("player", {"name": data})

                        if len(searching_player) > 0:
                            """check user if exists in self._data"""
                            if data in self._filter_name:
                                conn.send(Struct.USER_NOT_AVAILABLE)
                                continue

                        conn.send(Struct.JOIN_MESSAGE)
                        logger.debug(f"SEND JOIN: {Struct.JOIN_MESSAGE} TO {conn.getsockname()}")

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
                        self.executor.submit(self.handle_client, conn)
                        self._current_player +=1

                    logger.debug(f"SLEEPING THREAD BEFORE {th.current_thread().name}")
                    time.sleep(2)

                except EOFError as e:
                    logger.error(f"ERROR[{e}] CLIENT: {addr}" )

            except (OSError,BlockingIOError) as e:
                logger.error(f"ERROR[{e}] BlockingIOError")

    def _receive(self):
        logger.debug(f"START THREAD: ---[{th.current_thread().name}]")

        while True:
            try:
                data = q.get(timeout=1)

                if isinstance(data, dict):
                    """
                        QUEUE FOR NEW PLAYERS.
                    """
                    new_player:dict = data
                    current = new_player.get("position")

                    if new_player.get("deleted") is not None:
                        try:
                            self._data.pop(current)
                            self._sockets.remove(new_player.get("conn"))
                            self._filter_name.remove(new_player.get("name"))
                            logger.debug(f"Removed player at position {current}. THREAD: {th.current_thread().name}")
                        except (KeyError, ValueError) as e:
                            data.clear()
                            logger.error(f"ERROR DELETING DATA: {e}")
                        continue

                    others_players:Dict[int,dict] = self._data.copy()
                    self._data[current] = new_player

                    encoded_message = Struct.pack_player(None, new_player)
                    logger.debug(f"BEFORE SEND TO PLAYER INIT: {new_player}")
                    conn_new_player:socket.socket = new_player.get("conn")

                    """ADD NEW CONN"""
                    self._sockets.append(conn_new_player)
                    conn_new_player.send(encoded_message)

                    """SENDING OLD_PLAYERS TO NEW_PLAYER."""
                    conn_new_player.send(Struct.pack_players(others_players,Struct.OLD_PLAYER))

                    if len(others_players) > 0:
                        """SENDING NEW_PLAYER TO OTHER OLD PLAYERS"""
                        for position, player in others_players.items():
                            conn: socket.socket = player.get("conn")
                            encoded_message = Struct.pack_player(None, new_player, Struct.NEW_PLAYER)
                            conn.send(encoded_message)

                elif isinstance(data,bytes):
                    """
                        QUEUE FOR OLD PLAYERS
                    """
                    if time.time() - self.tick_last_sent >= TICK_RATE:
                        self.tick_last_sent = time.time()
                        for conn in self._sockets:
                            """FOR MOMENTS USES 'self._data', soon only modify data."""
                            self.executor.submit(send_data, conn,Struct.pack_players(self._data))

            except queue.Empty:
                continue

            except KeyboardInterrupt:
                self._socket.close()
                logger.warning(f"CLOSING SERVER IN MAIN THREAD...{th.current_thread().name}")
                sys.exit(1)

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
