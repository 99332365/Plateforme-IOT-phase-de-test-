import socket
import time

class WiFiServer:
    def __init__(self):
        # Configuration réseau Wi-Fi et serveur
        self.addr = '10.89.2.196'  # Adresse IP du FiPy
        self.port = 1234  # Port d'écoute

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.addr, self.port))
        s.listen(1)
        print(f"Serveur Wi-Fi en écoute sur {self.addr}:{self.port}")

        conn, _ = s.accept()
        print("Connexion Wi-Fi acceptée")
        data = conn.recv(1024).decode()

        if data.startswith("Temperature:"):
            temperature = data.split(":")[1].strip()
            print(f"Température Wi-Fi reçue: {temperature}")
            return temperature

        conn.close()

