'''
    brightness monitor for IPCP
'''
import os
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
                "brightness": bool
            }
        '''
        brightness = self.D0_INPUT.value
        self.brightness = {
            "brightness": brightness
        }
        return self.brightness
    
    def control_the_light(self, brightness=True):
        '''
            control the light applying to the plant
        '''
        status = "on" if not brightness else "off"
        os.system(f"sudo uhubctl -l 1-1 -p 2 -a {status}")

    