'''
    brightness monitor for IPCP
'''
import time

from gpiozero import DigitalInputDevice


class BrightnessMonitor:
    '''
        Brightness Monitor class for IPCP
    '''
    def __init__(self):
        self.D0_PORT = 18
        self.D0_INPUT = DigitalInputDevice(self.D0_PORT)

    def show_brightness(self):
        '''
            return {
                "brightness": float
            }
        '''
        brightness = self.D0_INPUT.value
        self.brightness = {
            "brightness": brightness
        }
        return self.brightness
    