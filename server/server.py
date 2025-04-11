import socket
import threading as th
import time
import sys
import os
import queue
import logging
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict

from battle_tanks.components.collision import Collision
from .conexions import DatabaseManager
from battle_tanks.commons.package import Struct

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
TICK_RATE = 1/60

def send_data(conn:socket.socket, data:bytes):
    try:
        conn.sendall(data)
    except (TimeoutError,ConnectionResetError,BrokenPipeError) as e:
        logger.error(f"SEND DATA FAILED: {data}. TO:{th.current_thread().name}. EXCEPT:{e}")


def split_bytes(byte_sequence) -> List[bytes]:
    return [byte_sequence[i:i+Struct.BUFFER_SPLIT_MAP] for i in
            range(0, len(byte_sequence),Struct.BUFFER_SPLIT_MAP)]


class Server:
    """
    Server made in socket TCP
    TODO: socket with udp for players moves.
    """

    def __init__(self,addr, lvl_map_tmx:str):
        self.tick_last_sent = time.time()
        self._data:Dict[int,dict] = defaultdict(dict)
        self._buffer_state_events = []
        self._sockets = []

        self._filter_name:list = []
        self._current_player = 0

        self._socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self._socket.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1)
        self._socket.bind(addr)
        self.positions = {}

        self._max_players = Struct.MAX_PLAYERS
        self._executor = ThreadPoolExecutor(max_workers=10,thread_name_prefix="CLIENT_RECV")
        self._socket.listen(self._max_players)

        DatabaseManager.configure({"database_name":"database.json"})
        self.persistence = DatabaseManager.get()

        Collision.load(lvl_map_tmx, Struct.pack_tile)
        
        """
        GAME STATE FOR OBJECTS.
        """

        th_1 = th.Thread(target = self._conexions, daemon = True)
        th_2 = th.Thread(target=self._handle_menu, daemon = True)
        th_2.start()
        th_1.start()

        self._receive()


    def _get_position(self,current) -> tuple:
        if self.positions.get(current) is None:
            return 323,677

        return self.positions.get(current)


    def _handle_menu(self):
        logger.debug(f"INIT HANDLE_MENU {th.current_thread().name}")
        while True:
            try:
                op = input("\n>")
                if op == "users":
                    for player in Collision.players:
                        print(player.get("name"))
                elif op == "data":
                    for data in self._data.items():
                        print(data)
                elif op == "bricks":
                    print(Collision.bricks)
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


    def _handle_client(self,client_socket: socket.socket):
        logger.warning(f"RUNNING NEW THREAD CLIENT: {client_socket.getsockname()} - THREAD -- {th.current_thread().name}")
        while True:
            try:
                data = client_socket.recv(Struct.BUFFER_SIZE_EVENT)
                if not data:
                    position = self._get_player_position(client_socket)
                    if position == -1:
                        break

                    player = self._data[position]
                    # Guardar la posición antes de marcar como eliminado
                    self.persistence.update("player", 
                        {"name": player.get("name")},
                        {
                            "x": player.get("x"),
                            "y": player.get("y"),
                            "angle": player.get("angle"),
                            "angle_cannon": player.get("angle_cannon")
                        }
                    )
                    player["deleted"] = True
                    q.put(player)

                if data == Struct.CLOSE_CONN:
                    logger.warning(f"CLOSED: {client_socket.getsockname()} "
                                   f"THREAD -- {th.current_thread().name}")

                    for position, player in self._data.items():
                        if client_socket == player.get("conn"):
                            # Guardar la posición antes de marcar como eliminado
                            self.persistence.update("player", 
                                {"name": player.get("name")},
                                {
                                    "x": player.get("x"),
                                    "y": player.get("y"),
                                    "angle": player.get("angle"),
                                    "angle_cannon": player.get("angle_cannon")
                                }
                            )
                            player["deleted"] = True
                            q.put(player)

                position = self._get_player_position(client_socket)
                if position >= 0:
                    player_data: dict = self._data[position]
                    """
                    FIX THAT
                    """

                    if data in Struct.MOVES:
                        # Validar colisiones después del movimiento
                        if data == Struct.UP_EVENT_PLAYER or data == Struct.DOWN_EVENT_PLAYER:
                            Collision.collide_with_objects(player_data)
                        
                        # Enviar la posición validada al cliente
                        encoded_message = Struct.pack_player(data, player_data)
                        q.put(encoded_message)

                    elif data == Struct.FIRE_EVENT_PLAYER:
                        encoded_message = Struct.pack_event(player_data)
                        if encoded_message:
                            if len(encoded_message) == Struct.SIZE_PLAYER:
                                q.put(Struct.OK_MESSAGE + encoded_message)
                            else:
                                q.put(encoded_message)

            except (ConnectionResetError, ConnectionRefusedError, socket.error) as e:
                logger.error(f"LOG ERROR: {e}")
                print(f"ERROR IN SOCKET: {e}")

                for position, player in self._data.items():
                    if client_socket == player.get("conn"):
                        player["deleted"] = True
                        q.put(player)

                client_socket.close()
                break

            except Exception as e:
                print(e)
                print(f"THREAD IS: {th.current_thread().is_alive()}")
                print("SOCKET FAILED!")
                print(f"SIZE: {q.qsize()}")
                print(f"EMPTY: {q.empty()}")

                for position, player in self._data.items():
                    if client_socket == player.get("conn"):
                        player["deleted"] = True
                        q.put(player)

                client_socket.close()
                break


    def _conexions(self):
        logger.warning(f"WAITING CONEXIONS --- {th.current_thread().name}")
        while True:
            try:
                if len(self._data) >= self._max_players:
                    time.sleep(10)
                    continue

                conn,addr = self._socket.accept()
                conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                conn.send(Struct.OK_MESSAGE)
                data = conn.recv(Struct.BUFFER_SIZE_NAME)

                try:
                    if data != b'': #NAME PLAYER
                        data = Struct.unpack(data)
                        logger.warning(f"ADD NEW_CONEXIONS: {data}")
                        if data.find("-c") > -1:
                            if data[:-2] in self._filter_name:
                                conn.send(Struct.USER_NOT_AVAILABLE)
                            conn.send(Struct.OK_MESSAGE)
                            continue

                        current = list(set(range(self._max_players)) - set([position for position, _ in self._data.items()]))[0]
                        searching_player = self.persistence.find("player", {"name": data})

                        if len(searching_player) > 0:
                            """check user if exists in self._data"""
                            if data in self._filter_name:
                                logger.debug(f"NAME IN DATA: {self._filter_name} TO: {Struct.USER_NOT_AVAILABLE}")
                                conn.send(Struct.USER_NOT_AVAILABLE)
                                continue

                        conn.send(Struct.pack(Collision.lvl_map))

                        logger.debug(f"SEND JOIN: {Struct.JOIN_MESSAGE} TO {conn.getsockname()}")

                        if len(searching_player) == 0:
                            x,y = self._get_position(current)
                            player = self.persistence.save(
                                "player",{
                                    "damage_indicator":0,
                                    "name": data,
                                    "position": current,
                                    "x": x,
                                    "y": y,
                                    "cannon_x":338,
                                    "cannon_y":692,
                                    "angle":0,
                                    "angle_cannon":0
                                })
                        else:
                            player = searching_player[0]
                            player["addr"] = addr
                            # Usar la posición guardada del jugador
                            x = player.get("x", self._get_position(current)[0])
                            y = player.get("y", self._get_position(current)[1])
                            player["x"] = x
                            player["y"] = y
                            player["position"] = current

                        player["conn"] = conn
                        """Current Player in Queue."""
                        q.put(player)
                        self._executor.submit(self._handle_client, conn)
                        self._current_player +=1

                    logger.debug(f"SLEEPING THREAD BEFORE {th.current_thread().name}")
                    time.sleep(4)

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
                    """QUEUE FOR NEW PLAYERS."""
                    if len(data.keys()) == 0:
                        continue

                    new_player:dict = data
                    current = new_player.get("position")

                    if new_player.get("deleted") is not None:
                        try:
                            self._data.pop(current)
                            self._sockets.remove(new_player.get("conn"))
                            self._filter_name.remove(new_player.get("name"))
                            Collision.players.remove(new_player)
                            logger.debug(f"Removed player at position {current}. THREAD: {th.current_thread().name}")
                            continue
                        except (KeyError, ValueError) as e:
                            data.clear()
                            logger.error(f"DELETING DATA: {e}")
                            continue

                    others_players: Dict[int, dict] = self._data.copy()
                    logger.debug(f"BEFORE SEND TO PLAYER INIT: {new_player}")

                    try:
                        conn_new_player: socket.socket = new_player.get("conn")
                        encoded_message = Struct.pack_player(None, new_player)
                        """ADD NEW CONN"""
                        conn_new_player.sendall(encoded_message)

                        """SENDING MAP OBJECTS"""
                        _game_state = split_bytes(Collision.game_state)
                        conn_new_player.sendall(Struct.pack_single_data(len(_game_state)))

                        for data in _game_state:
                            conn_new_player.sendall(data)

                        self._data[current] = new_player
                        self._filter_name.append(new_player.get("name"))
                        Collision.add_player(new_player)
                        self._sockets.append(conn_new_player)
                        
                    except socket.error as e:
                        del new_player
                        continue

                    if len(others_players) > 0 and new_player is not None:
                        """SENDING NEW_PLAYER TO OTHER OLD PLAYERS"""
                        for position, player in others_players.items():
                            conn: socket.socket = player.get("conn")
                            encoded_message = Struct.pack_player(None, new_player, Struct.NEW_PLAYER)
                            try:
                                conn.send(encoded_message)
                            except socket.error:
                                logger.error(f" IN {th.current_thread().name} FAILED PLAYER: {player}")
                                player["deleted"] = True
                                q.put(player)

                elif isinstance(data,bytes):
                    """QUEUE FOR OLD PLAYERS"""
                    if len(data) == Struct.BUFFER_SIZE_EVENT_RESPONSE:
                        # Enviar inmediatamente las actualizaciones de movimiento
                        for conn in self._sockets:
                            self._executor.submit(send_data, conn, data)
                    else:
                        # Para otros tipos de datos, mantener el tick rate
                        current_time = time.time()
                        if current_time - self.tick_last_sent >= TICK_RATE:
                            self.tick_last_sent = current_time
                            for conn in self._sockets:
                                self._executor.submit(send_data, conn, Struct.pack_players(self._data))

            except (queue.Empty, ConnectionAbortedError) as e:
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

