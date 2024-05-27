from flask import Flask, render_template, redirect, url_for, request
import requests
import json

from REST.get import RestGet
from REST.post import RestPost
from REST.login import RestSign
from Modbus.modbus import ModbusConn

app = Flask(__name__)

global token
token = '1'


@app.route('/')  # route handler 함수
def index():
    return redirect(url_for('new_mission'))


@app.route('/login')
def login():
    try:
        uri_login = 'http://127.0.0.1:8081/wms/monitor/session/login?username=admin&pwd=123456'
        response = requests.get(uri_login).json()
        new_token = response["payload"]["sessiontoken"]
    except requests.ConnectionError:
        print()
        return render_template('error503.html')

    global token
    token = json.dumps(new_token)
    token = token.replace('"', '')

    return RestSign.after_login(token)


@app.route('/alarm', methods=['GET'])
def alarm():
    result = RestGet().get_alarm(token)
    return result


@app.route('/vehicle', methods=['GET'])
def vehicle():
    return render_template('vehicle.html', token=token)


@app.route('/vehicle', methods=['POST'])
def vehicle_post():
    result = RestPost().insert_vehicle(token)
    return result


@app.route('/new-mission', methods=['GET'])
def new_mission():
    return render_template('new-mission.html')


@app.route('/new-mission', methods=['POST'])
def new_mission_post():
    result = RestPost().new_mission(token)
    return result


@app.route('/data', methods=['GET'])
def modbus_data():
    regs = ModbusConn().read_regs()
    return render_template('data-received.html', regs=regs)


@app.route('/setting', methods=['GET'])
def setting():
    return 0


@app.route('/setting', methods=['POST'])
def setting_post():
    return 0


@app.route('/503', methods=['GET'])
def error503():
    return render_template('error503.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
    # app.run(host='127.0.0.1', port=8080, debug=True)
    # 로컬호스트 테스트 필요

