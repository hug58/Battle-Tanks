#!/usr/bin/python3
import socket as s
import os
from server_tcp import server 




if __name__ == '__main__':


	port = 10030

	if os.name != 'posix':
	
		host_name = s.gethostname()
		host_ip = s.gethostbyname(host_name)


	else:
		
		host_name = s.gethostname()		
		host_ip = s.gethostbyname(host_name)

		if host_ip == '127.0.1.1':
			host_ip = input('INTRODUCE TO IP: ')


	print('IP THE SERVER: {ip}'.format(ip = host_ip))
	print('PORT : {port}'.format(port = port))

	server.main(port,host_ip)
