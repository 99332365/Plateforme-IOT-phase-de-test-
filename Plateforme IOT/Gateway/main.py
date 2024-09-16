import _thread
import time
from ble_server import BLEServer
from wifi_server import WiFiServer
from lora_server import LoRaServer

def gerer_wifi(wifi_server):
    print("Serveur Wi-Fi démarré")
    wifi_server.run()

def gerer_ble(ble_server):
    print("Serveur BLE démarré")
    ble_server.run()

def gerer_lora(lora_server):
    print("Serveur LoRa démarré")
    lora_server.run()

def main():
    # Initialiser les serveurs pour Wi-Fi, BLE, et LoRa
    wifi_server = WiFiServer()
    ble_server = BLEServer()
    lora_server = LoRaServer()

    # Démarrer chaque serveur dans un thread séparé pour assurer la simultanéité
    _thread.start_new_thread(gerer_wifi, (wifi_server,))
    _thread.start_new_thread(gerer_ble, (ble_server,))
    _thread.start_new_thread(gerer_lora, (lora_server,))

    try:
        # Boucle principale qui garde le programme actif
        while True:
            time.sleep(1)  # Garde le programme en cours d'exécution
    except KeyboardInterrupt:
        print("Arrêt des serveurs")

if __name__ == "__main__":
    main()
