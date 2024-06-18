'''
    humidity monitor for IPCP
'''
from time import sleep

import Adafruit_DHT as dht
from gpiozero import DigitalInputDevice
import RPi.GPIO as GPIO


class HumidityMonitor:
    '''
        Humidity Monitor class for IPCP
    '''

    def __init__(self):
        self.turn_on_pump = False
        self.humidity = {}
        self.DHT11_PORT = 4
        self.YL69_PORT = 5
        self.PUMP_PORT = 14

    def show_humidity(self):
        '''
            return {
                "humidity": float,
                "temperature": float,
                "soil_humidity_threshold": bool
            }
        '''
        # Read Humidity and Temperature from DHT11
        DHT_humidity, _ = dht.read_retry(dht.DHT11, self.DHT11_PORT)
        # Read Humidity from YL69, 0 means wet, 1 means dry
        soil_humidity_threshold = DigitalInputDevice(self.YL69_PORT)
        self.humidity = {
            "humidity": DHT_humidity,
            "soil_humidity_threshold": soil_humidity_threshold.value
        }
        del DHT_humidity, soil_humidity_threshold
        return self.humidity

    def switch_pump(self):
        '''
            switch pump
                - GPIO.HIGH: turn off
                - GPIO.LOW:  turn on
        '''
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PUMP_PORT, GPIO.OUT)
        GPIO.output(self.PUMP_PORT, GPIO.HIGH)
        msg = ''
        # to get self.humidity data
        self.show_humidity()

        msg = 'The plant is not dry'
        if self.humidity["soil_humidity_threshold"]:
            GPIO.output(self.PUMP_PORT, GPIO.LOW)
            self.turn_on_pump = True
            # Turn off pump after 4 seconds
            sleep(4)
            GPIO.output(self.PUMP_PORT, GPIO.HIGH)
            self.turn_on_pump = False
            msg = 'The plant has been watered'

        return {
            **self.humidity,
            "message": msg
        }


if __name__ == '__main__':
    h = HumidityMonitor()
    print(h.show_humidity())
    print(h.switch_pump())
