import socket
import time

class LoRaServer:
    def __init__(self):
        # Adresse IP du serveur LoRa
        self.addr = '10.89.2.198'  # Adresse IP du FiPy
        self.port = 1236  # Port d'écoute LoRa

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.addr, self.port))
        s.listen(1)
        print(f"Serveur LoRa en écoute sur {self.addr}:{self.port}")

        conn, _ = s.accept()
        print("Connexion LoRa acceptée")
        data = conn.recv(1024).decode()

        if data.startswith("Temperature:"):
            temperature = data.split(":")[1].strip()
            print(f"Température LoRa reçue: {temperature}")
            return temperature

        conn.close()
