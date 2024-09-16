from network import Bluetooth
import time

# Initialiser la connexion BLE
def envoyer_donnees_ble():
    ble = Bluetooth()
    ble.set_advertisement(name="BLE_Client", service_uuid=b'1234567890123456')
    ble.advertise(True)
    
    temperatures = [20.0, 21.5, 22.3, 23.1, 24.0, 25.2, 26.1, 27.5, 28.0, 29.3]
    index = 0

    while True:
        try:
            if ble.isconnected():
                temperature = temperatures[index]
                data_to_send = "Temperature: {}\n".format(temperature)
                print('Données BLE envoyées: {}'.format(data_to_send.strip()))

                # Simuler envoi des données (remplacez par votre envoi BLE réel)
                time.sleep(5)

            index = (index + 1) % len(temperatures)

        except Exception as e:
            print('Erreur d\'envoi BLE: {}'.format(e))

envoyer_donnees_ble()
