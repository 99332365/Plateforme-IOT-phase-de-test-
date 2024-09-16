from network import Bluetooth
import time

class BLEServer:
    def __init__(self):
        self.ble = Bluetooth()
        self.ble.set_advertisement(name='FiPy_BLE', manufacturer_data='123456')
        self.ble.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED, handler=self.conn_cb)
        self.conn_handle = None

    def conn_cb(self, bt_o, event):
        if event == Bluetooth.CLIENT_CONNECTED:
            print('Client BLE connecté')
        elif event == Bluetooth.CLIENT_DISCONNECTED:
            print('Client BLE déconnecté')

    def receive_data(self):
        self.ble.advertise(True)
        while True:
            if self.ble.irq():
                conn = self.ble.irq().recv(512)
                if conn:
                    data = conn.decode('utf-8').strip()
                    print('Données BLE reçues: {data}')
                    return data
            time.sleep(1)
