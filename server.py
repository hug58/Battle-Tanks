#!/usr/bin/python3
import socket
import os
from scripts.server import Server 


if __name__ == "__main__":
    port = 10030
    if os.name != "posix":
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
    else:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        if host_ip == "127.0.1.1":
            host_ip = input("INTRODUCE TO IP: ")

    print(f"NAME: {host_name}")
    print(f"IP THE SERVER: {host_ip}")
    print(f"PORT : {port}")
    Server((host_ip,port))
