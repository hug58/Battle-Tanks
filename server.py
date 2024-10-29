#!/usr/bin/python3
import socket
import os
from server import Server 


if __name__ == '__main__':

	ip_bind = os.getenv("IP_BIND","0.0.0.0")
	port = os.getenv("SERVER_PORT",8500)

	print('IP THE SERVER: {ip}'.format(ip = ip_bind))
	print('PORT : {port}'.format(port = port))
	Server((ip_bind,port))
