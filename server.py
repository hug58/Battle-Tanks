#!/usr/bin/python3

import os
from server import Server 

if __name__ == "__main__":
	ip_bind = os.getenv("IP_BIND", "0.0.0.0")
	port = os.getenv("SERVER_PORT", 8010)
	lvl_map = os.getenv("MAP", "assets/maps/zone_0.tmx")

	print(f"IP THE SERVER: {ip_bind}")
	print(f"PORT : {port}")
	print(f"MAP : {lvl_map}")
	Server((ip_bind, port), lvl_map)
