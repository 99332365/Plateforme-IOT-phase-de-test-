from network import LoRa
import socket
import time

class LoRaServer:
    def __init__(self, frequency, spreading_factor, bandwidth, coding_rate):
        self.lora = LoRa(mode=LoRa.LORA, frequency=frequency, sf=spreading_factor, bandwidth=bandwidth, coding_rate=coding_rate)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', 1236))  # Port pour recevoir les données LoRa

    def run(self):
        print('Serveur LoRa en attente des données...')
        while True:
            data, addr = self.sock.recvfrom(1024)
            if data:
                message = data.decode('utf-8').strip()
                print('Données LoRa reçues: {message}')
                return message
            time.sleep(1)
