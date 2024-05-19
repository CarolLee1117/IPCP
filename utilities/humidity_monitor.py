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
        self.DHT22_PORT = 4
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
        # Read Humidity and Temperature from DHT22
        DHT_humidity, DHT_temperature = dht.read_retry(dht.DHT22, self.DHT22_PORT)
        # Read Humidity from YL69, 0 means wet, 1 means dry
        soil_humidity_threshold = DigitalInputDevice(self.YL69_PORT)
        self.humidity = {
            "humidity": DHT_humidity,
            "temperature": DHT_humidity,
            "soil_humidity_threshold": soil_humidity_threshold.value
        }
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

        if self.humidity["soil_humidity_threshold"]:
            GPIO.output(self.PUMP_PORT, GPIO.LOW)
            self.turn_on_pump = True
            # Turn off pump after 5 seconds
            sleep(5)
            GPIO.output(self.PUMP_PORT, GPIO.HIGH)
            self.turn_on_pump = False
            msg = 'The plant has been watered'
        else:    
            msg = 'The plant is not dry'

        return {
            "turn_on_pump": self.turn_on_pump,
            "message": msg
        }

