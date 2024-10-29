
import socket
import threading as th 
import time 
import os
from .common import _unpack,_pack,BUFFER_SIZE


class Server:
    """Server made in socket TCP"""
    def __init__(self,addr):
        self._clients = []
        self._data = {}
        self._current_player = 0
        self._socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self._socket.bind(addr)
        self._socket.listen(10)
        self._max_players = 2
        # self._socket.setblocking(False)

        th_1 = th.Thread(target = self._conexions,daemon = True)
        th_1.start()
        th_2 = th.Thread(target = self._recevie,daemon = True)
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
                    break
                elif op in ("help","h"): 
                    print("OPTIONS: users and data")
            except KeyboardInterrupt:
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
                print("testeando")
                conn.send(_pack("OK"))
                data = conn.recv(BUFFER_SIZE)
                data = _unpack(data)

                print("client: " + data)

                if data == "CONNECT_PARTY":
                    current = list(set(range(self._max_players))
                                   -set([addr[1] for _,addr in self._clients]))[0]
                    conn.send(_pack(current))
                    client = (conn,[addr,current])
                    self._clients.append(client)
                    self._current_player +=1
                    # self._clients.append((conn,addr))


            except BlockingIOError as error:
                print(f"error waiting for connections {error}")


    def _recevie(self):
        while True:
            if len(self._clients) > 1:
                for conn,addr in self._clients:
                    try:
                        data = conn.recv(BUFFER_SIZE)
                        data = _unpack(data)
                        data.num_player = addr[1]
                        self._data[data.num_player] = data
                        self._messages_client(data,conn)
                    except ConnectionResetError as error:
                        print(f"error in conexion, deleting player: {error}")
                        self._data.pop(addr[1])
                        self._clients.remove((conn,addr))
                    except BlockingIOError as error:
                        print(f"error connect {error}")
                        self._data.pop(addr[1])
                        self._clients.remove((conn,addr))
                    except EOFError as error:
                        print(f"error in data: {error}")
                        time.sleep(3)
                        try:
                            self._data.pop(addr[1])
                        except KeyError as e:
                            print(f"error in delete player {e}")
                        self._clients.remove((conn,addr))
                    except ConnectionAbortedError as error:
                        print(f"error connect {error}")
                    except BrokenPipeError as e:
                        print(f"Connection aborted: {e}")
                        print("Conexions List: " + str(self._clients) )



    def _messages_client(self,data,client):
        data_pack = _pack(data)		
        for conn,i in self._clients:
            if conn == client:
                continue

            conn.send(data_pack)



if __name__ == '__main__':
    ip_bind = os.getenv("IP_BIND","0.0.0.0")
    port = os.getenv("SERVER_PORT",8500)

    print('IP THE SERVER: {ip}'.format(ip = ip_bind))
    print('PORT : {port}'.format(port = port))
    Server((ip_bind,port))
