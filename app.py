'''
做一個簡單的伺服器
'''
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    """
    這個函式會回傳 "Hello World!" 字串
    """
    return 'Hello World!'


@app.route('/adjust_light_auto')
def adjust_light_auto():
    """
    - 控制模組
    這個函式會回傳 "adjust_light_auto" 字串
    """
    return 'adjust_light_auto'


@app.route('/pump_auto')
def pump_auto():
    '''
    - 控制模組
    這個函式會回傳 "pump_auto" 字串
    '''
    return 'pump_auto'


@app.route('/pump_manual')
def pump_manual():
    '''
    - 控制模組
    這個函式會回傳 "pump_manual" 字串
    '''
    return 'pump_manual'


@app.route('/get_temperature')
def get_temperature():
    '''
    - 溫度監測
    這個函式會回傳 "get_temperature" 字串
    '''
    return 'get_temperature'


@app.route('/get_brightness')
def get_brightness():
    '''
    - 亮度監測
    這個函式會回傳 "get_brightness" 字串
    '''
    return 'get_brightness'


@app.route('/get_humidity')
def get_humidity():
    '''
    - 濕度監測
    這個函式會回傳 "get_humidity" 字串
    '''
    return 'get_humidity'


@app.route('/get_plant_status')
def get_plant_status():
    '''
    - 遠端控制
    這個函式會回傳 "get_plant_status" 字串
    '''
    return 'get_plant_status'


@app.route('/pump_manual_remote')
def pump_manual_remote():
    '''
    - 遠端控制
    這個函式會回傳 "pump_manual_remote" 字串
    '''
    return 'pump_manual'


@app.route('/swich_light_remote')
def swich_light_remote():
    '''
    - 遠端控制
    這個函式會回傳 "swich_light_remote" 字串
    '''
    return 'swich_light'


@app.route('/update_ngrok_service')
def update_ngrok_service():
    '''
    - 動態更新 IP
    這個函式會回傳 "update_ngrok_service" 字串
    '''
    return 'update_ngrok_service'


@app.route('/send_email')
def send_email():
    '''
    - 動態更新 IP
    這個函式會回傳 "send_email" 字串
    '''
    return 'send_email'


if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )

