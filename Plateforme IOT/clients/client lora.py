from network import LoRa
import socket
import time

# Initialiser la connexion LoRa
def envoyer_donnees_lora():
    lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
    lora_sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    lora_sock.setblocking(False)

    temperatures = [20.0, 21.5, 22.3, 23.1, 24.0, 25.2, 26.1, 27.5, 28.0, 29.3]
    index = 0

    while True:
        try:
            temperature = temperatures[index]
            data_to_send = "Temperature: {}\n".format(temperature)
            lora_sock.send(data_to_send)
            print('Données LoRa envoyées: {}'.format(data_to_send.strip()))

            index = (index + 1) % len(temperatures)
            time.sleep(10)  # Attendre avant d'envoyer à nouveau

        except Exception as e:
            print('Erreur d\'envoi LoRa: {}'.format(e))

envoyer_donnees_lora()
