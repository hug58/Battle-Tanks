import socket 
import json 

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.HOST = "localhost"
        self.PORT = 10030
        self.addr = (self.HOST,self.PORT)
        self.pos = self.connect()

        #print(self.id)

    def get_pos(self):
        return self.pos

    def connect(self):
        
        try:
        
            self.client.connect(self.addr)
            return self.client.recv(2048).decode("utf-8")
            #return json.loads(self.client.recv(2048))

        except:
            pass


    def send(self,data):
        try:
            #data = json.dumps(data)
            self.client.send(bytes(data,"utf-8"))

            return self.client.recv(2028).decode("utf-8")            
            #return json.loads(self.client.recv(2048))


        except socket.error as e:
            print(e)


#n = Network()

#print(n.send("Hello"))
#print(n.send("Working"))
