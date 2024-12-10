import socket
import threading
import time
import json


class ServerUDP:
    def __init__(self, addr, max_players=10):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


        self.server_socket.bind(addr)
        local_address = self.server_socket.getsockname()

        print(local_address)

        self.clients = {}  # {addr: player_data}
        self.max_players = max_players
        self.lock = threading.Lock()

        print(f"Servidor UDP iniciado en {addr}")
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def receive_messages(self):
        while True:
            try:
                data, client_addr = self.server_socket.recvfrom(1024)
                print(f"mensajeL {data}")
                if data == b'\x01':  # Manejo del mensaje binario específico
                    print(f"Mensaje 'ping' recibido de {client_addr}")
                    self.server_socket.sendto(b'\x02', client_addr)  # Responder con un mensaje binario, p. ej., b'\x02'


            except Exception as e:
                print(f"Error al recibir mensaje: {e}")



    def broadcast(self, message):
        data = json.dumps(message).encode()
        with self.lock:
            for client_addr in self.clients.keys():
                self.server_socket.sendto(data, client_addr)


if __name__ == "__main__":
    server = ServerUDP(("localhost", 25565))
    while True:
        time.sleep(1)
