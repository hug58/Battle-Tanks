#!/usr/bin/python3
import socket as s
from server_tcp import server 

if __name__ == '__main__':
    host_name = s.gethostname()
    host_ip = s.gethostbyname(host_name)
    port = 10030

    print(f'IP THE SERVER: {host_ip}')
    print(f'PORT : {port}')

    server.main(port,host_ip)
