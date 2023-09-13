#!/usr/bin/python3
import socket
import os
from scripts.server import Server 


if __name__ == '__main__':
	port = 10030
	if os.name != 'posix':
		host_name = socket.gethostname()
		host_ip = socket.gethostbyname(host_name)
	else:
		host_name = socket.gethostname()		
		host_ip = socket.gethostbyname(host_name)

		if host_ip == '127.0.1.1':
			host_ip = input('INTRODUCE TO IP: ')

	print(host_name)
	print('IP THE SERVER: {ip}'.format(ip = host_ip))
	print('PORT : {port}'.format(port = port))
	Server((host_ip,port))
