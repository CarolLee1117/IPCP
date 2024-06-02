'''
Use flask-restful to create a simple API
'''
from flasgger import Swagger
from flask import Flask
from flask_restful import Api, Resource, reqparse

from utilities import brightness_monitor, humidity_monitor, temperature_monitor

app = Flask(__name__)
api = Api(app)

app.config['SWAGGER'] = {
    'title': 'IPCP API',
    'uiversion': 3
}
swagger = Swagger(app)


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

