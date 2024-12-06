
import socket
import threading as th
import uuid
import time
import sys
import os
import queue
import logging

from typing import  Union,Dict
from scripts.sprites.player import Player
from .conexions import DatabaseManager
from scripts.commons.package import (Struct,
                                     OK_MESSAGE,
                                     BUFFER_SIZE_EVENT)

q = queue.Queue()
logger = logging.getLogger()
# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)


class Server:
    """Server made in socket TCP"""

    def __init__(self,addr):
        self._clients = []
        self._data:Dict[int,dict] = {}
        self._current_player = 0
        self._socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self._socket.bind(addr)
        self._max_players = 10
        self._socket.listen(self._max_players)

        DatabaseManager.configure({"database_name":"mongo",
                                   "db":"testing",
                                   "host":"localhost",
                                   "port":27017})

        self.persistence = DatabaseManager.get()
        self.room = str(uuid.uuid4())

        th_1 = th.Thread(target = self._conexions, daemon = True)
        th_2 = th.Thread(target = self._receive, daemon = True)

        th_1.start()
        th_2.start()


        while True:
            try:
                op = input("\n>")
                if op == "users":
                    for _,addr in self._clients:
                        print(addr[0])
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
        print("Waiting conexions ...")

        while True:
            try:
                if len(self._clients) >= self._max_players:
                    print(self._clients)
                    time.sleep(3)
                    continue

                conn,addr = self._socket.accept()
                conn.send(OK_MESSAGE)
                data = Struct.unpack(conn.recv(BUFFER_SIZE_EVENT))

                try:
                    if data != b'':
                        current = list(set(range(self._max_players))- set([addr[1] for _,addr in self._clients]))[0]

                        """SEND POSITION OF PLAYER"""
                        conn.send(Struct.pack(str(current)))

                        client = (conn,[addr,current])

                        searching_player = self.persistence.find("player", {"name": data})
                        if len(searching_player) == 0:
                            player = self.persistence.save(
                                "player",{
                                    # "status": "on",
                                    # "room_id":self.room,
                                    "name": data, "position": current,
                                    # "addr": addr,
                                    "x": 100,
                                    "y": 200,
                                })
                        else:
                            player = searching_player[0]
                            player["addr"] = addr

                        player.pop("_id")
                        if player.get("room_id"):

                            player.pop("room_id")
                        player.pop("addr")
                        player["conn"] = conn

                        self._clients.append(client)
                        self._data[current] = player

                        q.put(current)

                        self._current_player +=1

                except EOFError as e:
                    print(f"ERROR CLIENT: {conn, addr}" )
                    print(e)

            except BlockingIOError as e:
                print(f"error waiting for connections {e}")

    def _receive(self):
        """ Receive """
        while True:
            if len(self._clients) != 0 and q.empty():
                for conn,addr in self._clients:
                    try:
                        data:bytes = conn.recv(BUFFER_SIZE_EVENT)
                        if data != b'':
                            self._messages_client(data,addr[1])

                    except ConnectionResetError as e:
                        logger.warning("ConnectionResetError")
                        self._data.pop(addr[1])
                        self._clients.remove((conn,addr))
                    except BlockingIOError as e:
                        logger.warning("BlockingIOError")
                        self._data.pop(addr[1])
                        self._clients.remove((conn,addr))
                    except EOFError as e:
                        logger.warning("EOFError")
                        self._data.pop(addr[1])
                        self._clients.remove((conn,addr))
                    except ConnectionAbortedError as e:
                        logger.warning("ConnectionAbortedError")
                        self._data.pop(addr[1])
                        self._clients.remove((conn,addr))
                    except BrokenPipeError as e:
                        logger.warning("BrokenPipeError")
                        self._data.pop(addr[1])
                        self._clients.remove((conn,addr))

            elif not q.empty():
                current:int = q.get()
                new_player:dict = self._data[current]
                self._data.pop(current)
                others_players = self._data.copy()
                self._data[current] = new_player


                for conn,addr in self._clients:
                    try:
                        data:bytes = conn.recv(BUFFER_SIZE_EVENT)
                        if data != b'':
                            self._messages_client(data,addr[1])
                    except:
                        pass




    def _messages_client(self,data:Union[bytes,None], player_number:int) -> None:
        """ SEND ALL CLIENTS MESSAGES """

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
