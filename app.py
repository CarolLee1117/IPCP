'''
Use flask-restful to create a simple API
'''
import os
from time import sleep
from threading import Thread

from flasgger import Swagger
from flask import Flask
from flask_restful import Api, Resource

from utilities import dynamic_url_updater, brightness_monitor, humidity_monitor, temperature_monitor

app = Flask(__name__)
api = Api(app)

app.config['SWAGGER'] = {
    'title': 'IPCP API',
    'uiversion': 3
}
swagger = Swagger(app)


# 使用 multi-threading 監控環境，並自動開啟馬達或植物燈
def monitor_environment():
    '''
    使用 multi-threading 監控環境，並自動開啟馬達或植物燈
    '''
    h = humidity_monitor.HumidityMonitor()
    b = brightness_monitor.BrightnessMonitor()

    # 30 mins
    interval = 1800

    while True:
        try:
            humidity = h.show_humidity()
            if humidity["soil_humidity_threshold"]:
                h.switch_pump()

            brightness = b.show_brightness()
            b.control_the_light(not brightness["brightness"])
            sleep(interval)
        except KeyboardInterrupt:
            break


def update_ngrok_url():
    '''
    使用 multi-threading 監控 ngrok 啟動時間，並更新 Tunneling URL
    '''
    duu = dynamic_url_updater.dynamicUrlUpdater()
    # 7.5 hrs
    interval = 27000
    while True:
        try:
            duu.restart_ngrok()
            sleep(3) # wait for ngrok to start        
            print(duu.get_ngrok_url())
            sleep(interval)
        except KeyboardInterrupt:
            break
    os.system('killall ngrok')


# 啟動 multi-threading
t1 = Thread(target=update_ngrok_url)
t1.start()
t1.join()
t2 = Thread(target=monitor_environment)
t2.start()
t2.join()


# 取得環境參數（濕度、亮度、溫度）
class Environment(Resource):
    '''
    取得環境參數（濕度、亮度、溫度）
    '''
    def get(self):
        '''
        使用 GET 方法取得環境參數
        '''
        b = brightness_monitor.BrightnessMonitor()
        brightness = b.show_brightness()

        h = humidity_monitor.HumidityMonitor()
        humidity = h.show_humidity()

        t = temperature_monitor.TemperatureMonitor()
        temperature = t.show_temperature()
        return {
            'brightness': brightness,
            'humidity': humidity,
            'temperature': temperature
        }


# 開啟／關閉植物燈
class PlantLight(Resource):
    '''
    開啟／關閉植物燈
    '''
    def get(self, on_off):
        '''
        使用 GET 方法開啟／關閉植物燈
        '''
        b = brightness_monitor.BrightnessMonitor()
        b.control_the_light(bool(on_off))
        return {'status': 200}


# 開啟馬達
class Motor(Resource):
    '''
    開啟馬達
    '''
    def get(self):
        '''
        使用 GET 方法開啟馬達
        '''
        h = humidity_monitor.HumidityMonitor()
        h.switch_pump()
        return {'status': 200}


# 註冊各 Endpoints
api.add_resource(Environment, '/plant_env')
api.add_resource(PlantLight, '/plant_light/<on_off>')
api.add_resource(Motor, '/motor_on')

if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )

