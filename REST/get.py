from flask import Flask, render_template, redirect, url_for, request
import requests
import json


class RestGet:

    @staticmethod
    def render_vehicle(token):
        if token == "1":
            return redirect(url_for('login'))
        try:
            return render_template('vehicle.html')
        except requests.RequestException as err:
            print("Trying Login Again...")
            return redirect(url_for('login'))

    # 위에거랑 합쳐야할듯
    @staticmethod
    def check_login(token):
        if token == '1':
            print('Logging in')
            return -1  # return error

    @staticmethod
    def get_vehicle_data(token):
        try:
            return render_template('chart.html')
        except KeyError as err:
            return redirect(url_for('login', link=1))
        except requests.ConnectionError:
            return '503 Server Unavailable :('

    # 알람 요청
    @staticmethod
    def get_alarm(token):
        try:
            uri_get_alarm = 'http://127.0.0.1:8081/wms/rest/alarms?&sessiontoken=' + token
            response = requests.get(uri_get_alarm).json()

            evt = json.dumps(response["payload"]["alarms"][0]["eventname"])
            scid = json.dumps(response["payload"]["alarms"][0]["sourceid"])
            state = json.dumps(response["payload"]["alarms"][0]["state"])
            time1st = json.dumps(response["payload"]["alarms"][0]["firsteventat"])

            return render_template('alarm.html', eventName=evt, sourceID=scid, state=state, time1st=time1st)

        except KeyError as err:
            return redirect(url_for('login', link=1))
        except requests.ConnectionError:
            return '503 Server Unavailable :('

