# main.py -- put your code here!
import _thread
import time
import socket
from machine import Pin
from network import WLAN
from network import LoRa
from ble_server import BLEServer  # Hypothèse : vous avez une classe BLEServer
from config import *
# Configuration du réseau Wi-Fi
ssid = 'IoT IMT Nord Europe'
password = '72Hin@R*'

# Configuration LoRa
LORA_FREQUENCY = 868000000  # Europe
LORA_SPREADING_FACTOR = 7
LORA_BANDWIDTH = LoRa.BW_125KHZ
LORA_CODING_RATE = LoRa.CODING_4_5

def configurer_reseau_wifi():
    wlan = WLAN(mode=WLAN.STA)
    wlan.connect(ssid, auth=(WLAN.WPA2, password))

    while not wlan.isconnected():
        print('Connecting to Wi-Fi...')
        time.sleep(1)

    print('Connected to Wi-Fi')
    print('IP Address: {}'.format(wlan.ifconfig()[0]))

# Serveur TCP pour Wi-Fi
def serveur_tcp_wifi():
    wlan = WLAN(mode=WLAN.STA)
    addr = wlan.ifconfig()[0]
    port = 1234

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((addr, port))
    s.listen(1)

    print('Serveur TCP en écoute sur {}:{}'.format(addr, port))

    while True:
        conn, _ = s.accept()
        print('Connexion acceptée')

        try:
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break
                print('Données Wi-Fi reçues: {}'.format(data.strip()))

                if data.startswith('Temperature:'):
                    temperature = data.split(':')[1].strip()
                    envoyer_temperature_tcp_sender(temperature)
                else:
                    print('Message Wi-Fi reçu: {}'.format(data))

                conn.send('Message reçu et traité\n'.encode())
        except OSError as e:
            print('Erreur de connexion Wi-Fi: {}'.format(e))
        finally:
            conn.close()
            print('Connexion Wi-Fi fermée')

# Serveur BLE pour recevoir des données de température
def serveur_ble(ble_server):
    while True:
        data = ble_server.receive_data()
        if data:
            print("Données BLE reçues: {}".format(data))
            if data.startswith('Temperature:'):
                temperature = data.split(':')[1].strip()
                envoyer_temperature_tcp_sender(temperature)

# Serveur LoRa pour recevoir des données de température
def serveur_lora(lora):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((lora.ifconfig()[0], 1236))  # Utilisez un port pour LoRa
    while True:
        data, addr = s.recvfrom(1024)
        print("Données LoRa reçues: {}".format(data))
        if data.startswith('Temperature:'):
            temperature = data.decode().split(':')[1].strip()
            envoyer_temperature_tcp_sender(temperature)

# Fonction pour envoyer les données de température à un autre nœud
def envoyer_temperature_tcp_sender(temperature):
    command = 'Temperature: {}\n'.format(temperature)
    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(('10.89.1.86', 1235))  # Adresse IP et port du TcpSenderNode
        conn.send(command.encode())
        print('Température envoyée: {}'.format(command.strip()))
    except Exception as e:
        print("Erreur d'envoi de température: {}".format(e))
    finally:
        conn.close()

# Configurer le réseau et démarrer les serveurs
def main():
    # Wi-Fi et BLE
    configurer_reseau_wifi()
    
    # Créer une instance du serveur BLE
    ble_server = BLEServer()

    # Créer une instance pour LoRa
    lora = LoRa(mode=LoRa.LORA, frequency=LORA_FREQUENCY, bandwidth=LORA_BANDWIDTH, spreading_factor=LORA_SPREADING_FACTOR, coding_rate=LORA_CODING_RATE)

    # Lancer les serveurs sur des threads séparés
    _thread.start_new_thread(serveur_tcp_wifi, ())
    _thread.start_new_thread(serveur_ble, (ble_server,))
    _thread.start_new_thread(serveur_lora, (lora,))

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Arrêt des serveurs")

main()
