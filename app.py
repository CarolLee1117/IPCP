'''
Use flask-restful to create a simple API
'''
from ast import literal_eval
import json
import os
from time import sleep
from threading import Thread

from dotenv import load_dotenv
from flasgger import Swagger
from flask import Flask, render_template, request
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse

from utilities import dynamic_url_updater, brightness_monitor, humidity_monitor, temperature_monitor

app = Flask(__name__)
api = Api(app)
CORS(app)

app.config['SWAGGER'] = {
    'title': 'IPCP API',
    'uiversion': 3
}
swagger = Swagger(app)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

load_dotenv()


def update_ngrok_url():
    '''
    使用 multi-threading 監控 ngrok 啟動時間，並更新 Tunneling URL
    '''
    duu = dynamic_url_updater.DynamicUrlUpdater()
    # 7.5 hrs
    interval = literal_eval(os.getenv('UPDATE_NGROK_URL_INTERVEL'))
    while True:
        try:
            duu.restart_ngrok()
            sleep(3)  # wait for ngrok to start
            print(duu.get_ngrok_url())
            sleep(interval)
        except KeyboardInterrupt:
            break
    os.system('killall ngrok')


# 取得環境參數（濕度、亮度、溫度）
class Environment(Resource):
    '''
    取得環境參數（濕度、亮度、溫度）
    '''

    def get(self):
        '''
        使用 GET 方法取得環境參數
        '''
        try:
            b = brightness_monitor.BrightnessMonitor()
            brightness = b.show_brightness()

            h = humidity_monitor.HumidityMonitor()
            humidity = h.show_humidity()

            t = temperature_monitor.TemperatureMonitor()
            temperature = t.show_temperature()

            return {
                'status': 200,
                'brightness': brightness,
                'humidity': humidity,
                'temperature': temperature
            }
        except Exception as e:
            return {'status': 400, 'msg': str(e)}


# 開啟／關閉植物燈
class PlantLight(Resource):
    '''
    開啟／關閉植物燈
    '''

    def get(self):
        '''
        使用 GET 方法開啟／關閉植物燈
        '''
        on_off = request.args.get('on_off', default=-1, type=int)
        b = brightness_monitor.BrightnessMonitor()
        result = b.control_the_light(int(on_off))
        return {'status': 200, **result}


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
        result = h.switch_pump()
        return {'status': 200, **result}


# 自動模式切換
class AutoMode(Resource):
    '''
    自動模式切換
    '''
    start = False

    def get(self):
        '''
        使用 GET 方法自動模式切換
        on_off=1: 開啟自動模式, on_off=0: 關閉自動模式
        '''
        mode = request.args.get('on_off', default=-1, type=int)
        if mode == 1:
            AutoMode.start = True
            monitor_environment_thread = Thread(
                target=self.monitor_environment)
            monitor_environment_thread.setDaemon(True)
            monitor_environment_thread.start()
        elif mode == 0:
            AutoMode.start = False

        return {
            'status': 200,
            'msg': f"Switch to {('auto' if AutoMode.start else 'manual')} mode",
            'mode': int(AutoMode.start)
        }

    def monitor_environment(self):
        '''
        使用 multi-threading 監控環境，並自動開啟馬達或植物燈
        '''
        h = humidity_monitor.HumidityMonitor()
        b = brightness_monitor.BrightnessMonitor()

        # 30 mins
        interval = literal_eval(os.getenv('MONITOR_ENVIRONMENT_INTERVEL'))

        while AutoMode.start:
            try:
                humidity = h.show_humidity()
                if humidity["soil_humidity_threshold"]:
                    h.switch_pump()

                brightness = b.show_brightness()
                b.control_the_light(brightness["brightness"])

                # log the environment data
                print({**humidity, **brightness})
                sleep(interval)
            except KeyboardInterrupt:
                break
        print("Auto mode is off")


# 取得與植物名稱、照顧者名稱、照片連結路徑
class PlantProfile(Resource):
    '''
    GET 提供植物名稱、照顧者名稱、照片連結路徑
    POST 修改植物名稱、照顧者名稱、照片連結路徑
    '''

    def get(self):
        '''
        使用 GET 方法取得植物名稱、照顧者名稱、照片連結路徑
        '''
        with open('plant_profile.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        return {
            'status': 200,
            'plant_name': data['plant_name'],
            'care_taker': data['care_taker'],
            'photo_path': data['photo_path']
        }

    def post(self):
        '''
        使用 POST 方法修改植物名稱、照顧者名稱、照片連結路徑
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('plant_name', type=str)
        parser.add_argument('care_taker', type=str)
        parser.add_argument('photo_path', type=str)

        args = parser.parse_args()
        plant_name = args.get('plant_name', None)
        care_taker = args.get('care_taker', None)
        photo_path = args.get('photo_path', None)

        if not all([plant_name, care_taker, photo_path]):
            return {'status': 400, 'msg': 'Missing required fields'}

        with open('plant_profile.json', 'w', encoding='utf-8') as file:
            json.dump({
                'plant_name': plant_name,
                'care_taker': care_taker,
                'photo_path': photo_path
            }, file, ensure_ascii=False, indent=4)

        return {
            'status': 200,
            'plant_name': plant_name,
            'care_taker': care_taker,
            'photo_path': photo_path
        }


# 上傳照片
class UploadPicture(Resource):
    '''
    上傳照片
    '''

    def post(self):
        '''
        使用 POST 方法上傳照片
        '''
        if 'file' not in request.files:
            return {'status': 400, 'msg': 'No file part'}

        file = request.files['file']
        if file.filename == '':
            return {'status': 400, 'msg': 'No selected file'}

        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return {'status': 200, 'filename': filename}


# 註冊各 Endpoints
api.add_resource(Environment, '/plant_env')
api.add_resource(PlantLight, '/plant_light')
api.add_resource(Motor, '/motor_on')
api.add_resource(AutoMode, '/auto_mode')
api.add_resource(PlantProfile, '/plant_profile')
api.add_resource(UploadPicture, '/upload_picture')


# 顯示首頁
@ app.route('/')
def index():
    '''
    顯示首頁，回傳 index.html
    '''
    return render_template('index.html')


if __name__ == '__main__':
    # 設定 multi-threading 任務
    update_ngrok_thread = Thread(target=update_ngrok_url)
    # 設定為背景執行緒，當主執行緒結束時，背景執行緒也會跟著結束
    update_ngrok_thread.setDaemon(True)
    # 啟動 multi-threading 服務
    update_ngrok_thread.start()

    # 啟動 Flask Server
    # debug=True: 啟動 debug 模式
    # user_reloader=False: 不使用 reloader
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        use_reloader=False  # prevent the server from restarting which will send the email again
    )
