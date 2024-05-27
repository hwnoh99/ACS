from flask import Flask, render_template, redirect, url_for, request
import requests
import json


class RestGet:
    def __init__(self):
        self.base_uri = 'http://127.0.0.1:8081/wms/'

    # vehicle 리스트 출력
    def render_vehicle(self, token):
        if token == "1":
            return redirect(url_for('login'))
        try:
            uri_vehicles_info = self.base_uri + '/rest/vehicles?&sessiontoken=' + token
            response = requests.get(uri_vehicles_info).json()

            amrs = response["payload"]["vehicles"]
            return render_template('vehicle.html', items=amrs)

        except KeyError as err:
            print("Trying Login Again...")
            return redirect(url_for('login', link=1))
        except requests.ConnectionError:
            return '503 Server Unavailable :('

    # Get alarms
    def get_alarm(self, token):
        try:
            uri_get_alarm = self.base_uri + 'rest/alarms?&sessiontoken=' + token
            response = requests.get(uri_get_alarm).json()

            evt = json.dumps(response["payload"]["alarms"][0]["eventname"])
            scid = json.dumps(response["payload"]["alarms"][0]["sourceid"])
            state = json.dumps(response["payload"]["alarms"][0]["state"])
            time1st = json.dumps(response["payload"]["alarms"][0]["firsteventat"])
            return render_template('alarm.html', eventName=evt, sourceID=scid, state=state, time1st=time1st)

        except requests.RequestException as err:
            return redirect(url_for('login'))
        except KeyError as err:
            return redirect(url_for('login', link=1))
        except requests.ConnectionError:
            return '503 Server Unavailable :('

    # # Get data of vehicle
    # def get_vehicle_data(self, token):
    #     try:
    #         return render_template('chart.html')
    #     except KeyError as err:
    #         return redirect(url_for('login', link=1))
    #     except requests.ConnectionError:
    #         return '503 Server Unavailable :('