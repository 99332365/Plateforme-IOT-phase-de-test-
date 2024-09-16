from machine import Pin
import network
import socket
import time
from network import WLAN

# Configuration du réseau Wi-Fi
ssid = 'IoT IMT Nord Europe'
password = '72Hin@R*'

def configurer_wifi():
    wlan = WLAN(mode=WLAN.STA)
    wlan.connect(ssid, auth=(WLAN.WPA2, password))

    while not wlan.isconnected():
        print('Connecting to Wi-Fi...')
        time.sleep(1)

    print('Connected to Wi-Fi')
    print('IP Address: {}'.format(wlan.ifconfig()[0]))

# Envoie des données de température au serveur
def envoyer_donnees_wifi():
    temperatures = [20.0, 21.5, 22.3, 23.1, 24.0, 25.2, 26.1, 27.5, 28.0, 29.3]
    index = 0

    while True:
        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect(('10.89.2.196', 1234))  # IP du serveur
            temperature = temperatures[index]
            data_to_send = "Temperature: {}\n".format(temperature)
            conn.send(data_to_send.encode())
            print('Données Wi-Fi envoyées: {}'.format(data_to_send.strip()))

            index = (index + 1) % len(temperatures)
            time.sleep(5)

        except Exception as e:
            print('Erreur d\'envoi Wi-Fi: {}'.format(e))
        finally:
            conn.close()

# Configurer le réseau Wi-Fi et envoyer des données
configurer_wifi()
envoyer_donnees_wifi()
