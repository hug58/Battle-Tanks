import socket
import threading as th

from _thread import * 

import sys 
import json

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

pos = [(0,0),(100,100)]

def read_pos(str):
    str = str.split(",")
    return int(str[0]),int(str[1])       

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


def threaded_client(conn, player):
    
    conn.send(str.encode(make_pos(pos[player])))
    #conn.send(bytes(json.dumps("Connected"),"utf-8"))

    reply = ""

    while 1:
        try:
            data =   read_pos(conn.recv(2048).decode("utf-8"))
            pos[player] = data 
            #reply = data.decode("utf-8")


            if not data:
                print("Disconected")
                break

            else:

                if player == 1:
                    reply = pos[0]

                else:
                    reply = pos[1]

                #print("Recieved: ", data)
                #print("Sending: ", reply)

            #data = json.dumps(data)
            conn.sendall(str.encode(make_pos(reply)))

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
