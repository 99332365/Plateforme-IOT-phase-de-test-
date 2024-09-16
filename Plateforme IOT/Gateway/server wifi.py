import socket
from network import WLAN
import time

class WiFiServer:
    def __init__(self):
        self.wlan = WLAN(mode=WLAN.STA)

    def run(self):
        addr = self.wlan.ifconfig()[0]
        port = 1234

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((addr, port))
        s.listen(1)

        print('Serveur Wi-Fi en écoute sur {addr}:{port}')

        while True:
            conn, _ = s.accept()
            print('Connexion Wi-Fi acceptée')
            try:
                while True:
                    data = conn.recv(1024).decode()
                    if not data:
                        break
                    print('Données Wi-Fi reçues: {data.strip()}')
                    return data
            except OSError as e:
                print('Erreur de connexion Wi-Fi: {e}')
            finally:
                conn.close()
                print('Connexion Wi-Fi fermée')
