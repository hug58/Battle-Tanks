#!/usr/bin/python3

import os
from server import Server 


if __name__ == "__main__":

	ip_bind = "0.0.0.0"
	port = 8010

	print("SERVER IP: {ip}".format(ip = ip_bind))
	print("PORT: {port}".format(port = port))
	Server((ip_bind,port))
