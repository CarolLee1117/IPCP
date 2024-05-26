'''
    temperature monitor for IPCP
'''
from time import sleep

import Adafruit_DHT as dht


class TemperatureMonitor:
    '''
        Temperature Monitor class for IPCP
    '''
    def __init__(self):
        self.temperature = {}
        self.DHT22_PORT = 4

    def show_temperature(self):
        '''
            return {
                "temperature": float
            }
        '''
        # Read Temperature from DHT22
        _, DHT_temperature = dht.read_retry(dht.DHT22, self.DHT22_PORT)
        self.temperature = {
            "temperature": DHT_temperature
        }
        return self.temperature