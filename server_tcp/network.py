import socket 
import json 

from server_tcp import package

class Network:
    def __init__(self,HOST,PORT):
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        self.addr = (HOST,int(PORT))
        self.key = self.connect()

    def get_key(self):
        return self.key

    def connect(self):
        
        try:
            self.client.connect(self.addr)

            data_c = package.unpack(self.client.recv(2048))
            return data_c

        except:
            pass


    def send(self,data):
        try:
            data_s = package.pack(data)
            self.client.send(data_s)

            data_c = self.client.recv(2048)
            return package.unpack(data_c)

        except socket.error as e:
            print(e)
