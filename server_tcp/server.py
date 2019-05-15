import socket
import threading as th
import sys 
import json

from _thread import * 

import package

HOST = "localhost"
PORT = 10030


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

try:
    s.bind((HOST,PORT))

except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection, Server Started")

#pos = [(300,300),(60,300)]
key = {
	'SPACE': False,
	'LEFT': False,
	'RIGHT': False,
	'UP': False,

    'x': 300,
    'y': 300,

    'angle':0,

}

key_2 = {
	'SPACE': False,
	'LEFT': False,
	'RIGHT': False,
	'UP': False,
    
    'x': 60,
    'y': 60,

    'angle':0,

}

keys_players = [key,key_2]

# def read_pos(str):
#     str = str.split(",")
#     return int(str[0]),int(str[1])       

# def make_pos(tup):
#     return str(tup[0]) + "," + str(tup[1])


def threaded_client(conn, player):

    #data_s = package.pack(make_pos(pos[player]))
    data_s = package.pack(keys_players[player])
    conn.send(data_s)

    reply = ""

    while 1:
        try:
            data_c = package.unpack(conn.recv(2048))
            #data = read_pos(data_c)

            #pos[player] = data 
            data = data_c
            keys_players[player] = data

            if not data:
                print("Disconected")
                break

            else:

                if player == 1:
                    #reply = pos[0]
                    reply = keys_players[0]
                else:
                    #reply = pos[1]
                    reply = keys_players[1]

            #data_s = package.pack(make_pos(reply))
            data_s = package.pack(reply)
            conn.send(data_s)

        except socket.error as e:
            print(e)
            break

    print("Lost Connection ")
    conn.close()

currentPlayer = 0

while 1:

    conn,addr = s.accept()
    print("Connectd to", addr)

    #th.Thread( target = threaded_client,args= (conn,)).start()
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
