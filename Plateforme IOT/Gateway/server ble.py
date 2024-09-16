import socket
import time

class BLEServer:
    def __init__(self):
        # Adresse IP du serveur BLE
        self.addr = '10.89.2.197'  # Adresse IP du FiPy
        self.port = 1235  # Port d'écoute BLE

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.addr, self.port))
        s.listen(1)
        print(f"Serveur BLE en écoute sur {self.addr}:{self.port}")

        conn, _ = s.accept()
        print("Connexion BLE acceptée")
        data = conn.recv(1024).decode()

        if data.startswith("Temperature:"):
            temperature = data.split(":")[1].strip()
            print(f"Température BLE reçue: {temperature}")
            return temperature

        conn.close()
