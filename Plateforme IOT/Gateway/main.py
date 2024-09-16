import _thread
import time
import socket
from wifi_server import WiFiServer
from ble_server import BLEServer
from lora_server import LoRaServer

# Fonction pour envoyer des données de température au TcpSenderNode
def envoyer_temperature_tcp_sender(temperature):
    command = 'Temperature: {}\n'.format(temperature)
    try:
        # Connexion à l'adresse IP du nœud TcpSenderNode et envoi de la commande
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(('10.89.1.86', 1235))  # Adresse IP et port du TcpSenderNode
        conn.send(command.encode())
        print('Température envoyée: {}'.format(command.strip()))
    except Exception as e:
        print('Erreur d\'envoi de température: {}'.format(e))
    finally:
        conn.close()  # Fermer la connexion après envoi

# Gestion simultanée des serveurs Wi-Fi, BLE et LoRa
def gerer_wifi(wifi_server):
    print("Serveur Wi-Fi démarré")
    while True:
        temperature = wifi_server.run()
        envoyer_temperature_tcp_sender(temperature)

def gerer_ble(ble_server):
    print("Serveur BLE démarré")
    while True:
        temperature = ble_server.run()
        envoyer_temperature_tcp_sender(temperature)

def gerer_lora(lora_server):
    print("Serveur LoRa démarré")
    while True:
        temperature = lora_server.run()
        envoyer_temperature_tcp_sender(temperature)

def main():
    # Initialisation des serveurs pour Wi-Fi, BLE, et LoRa
    wifi_server = WiFiServer()
    ble_server = BLEServer()
    lora_server = LoRaServer()

    # Lancer chaque serveur dans un thread séparé pour assurer la simultanéité
    _thread.start_new_thread(gerer_wifi, (wifi_server,))
    _thread.start_new_thread(gerer_ble, (ble_server,))
    _thread.start_new_thread(gerer_lora, (lora_server,))

    try:
        # Boucle principale pour maintenir la passerelle active
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Arrêt des serveurs")

if __name__ == "__main__":
    main()
