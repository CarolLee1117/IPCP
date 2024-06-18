'''
    brightness monitor for IPCP
'''
import os
import subprocess
import time

from gpiozero import DigitalInputDevice


class BrightnessMonitor:
    '''
        Brightness Monitor class for IPCP
    '''

    def __init__(self):
        self.D0_PORT = 18

    def show_brightness(self):
        '''
            return {
                "brightness": bool
            }
        '''
        brightness = DigitalInputDevice(self.D0_PORT).value
        self.brightness = {
            "brightness": brightness
        }
        del brightness
        return self.brightness

    def control_the_light(self, brightness=False):
        '''
            control the light applying to the plant
            - brightness: True: turn on, False: turn off
        '''
        # to get self.brightness data
        self.show_brightness()
        if brightness == -1:
            result = subprocess.run(
                ['sudo', 'uhubctl', '-l', '1-1', '-p', '2'],
                stdout=subprocess.PIPE,
                check=False
            )
            status = result.stdout.split(b' ')[-1] \
                .decode('utf-8').replace('\n', '')
            status = "on" if status == "power" else "off"
        else:
            status = "on" if brightness else "off"
            os.system(f"sudo uhubctl -l 1-1 -p 2 -a {status}")
        msg = f"the light is turned {status}"

        return {
            **self.brightness,
            'msg': msg
        }
