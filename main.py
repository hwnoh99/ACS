from flask import Flask, render_template, redirect, url_for, request
import requests
import json

from REST.get import RestGet
from REST.post import RestPost

app = Flask(__name__)


token = '1'


@app.route('/')
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

    link = request.args.get('link')
    if link is None or 0:
        return redirect(url_for('vehicle'))
    elif link == '1':
        return redirect(url_for('alarm'))
    elif link == '2':
        return redirect(url_for('new_mission'))
    elif link == '3':
        return redirect(url_for('s', token))
    else:
        return "LNG" + link


@app.route('/alarm', methods=['GET'])
def alarm():
    result = RestGet.get_alarm(token)
    return result


@app.route('/vehicle', methods=['GET'])
def vehicle():
    result = RestGet.render_vehicle(token)
    return result


@app.route('/vehicle', methods=['POST'])
def vehicle_insert():
    result = RestPost.insert_vehicle(token)
    return result


@app.route('/new-mission', methods=['GET'])
def new_mission():
    return render_template('new-mission.html')


@app.route('/new-mission', methods=['POST'])
def new_mission_post():
    start = request.form['start']
    stop = request.form['stop']
    msn_type = request.form['type']
    submit_type = request.form['sb-type']
    # 데이터 구조 example: ([('type', '7'), ('start', '100'), ('stop', '200'), ('btn-type', 'create')])
    # ImmutableMultiDict

    if msn_type == '7':
        result = RestPost.new_mission(token, msn_type, submit_type, start, stop)
    return result


@app.route('/menu', methods=['GET'])
def graphs():
    result = RestGet.get_vehicle_data(token)
    return result


@app.route('/503', methods=['GET'])
def error503():
    return render_template('error503.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
    # app.run(host='127.0.0.1', port=8080, debug=True)
    # 로컬호스트 테스트 필요
