from flask import Flask, render_template, redirect, url_for, request
import requests
import json

# Tip: Post하면 request는 자동생성되고 각각의 함수에 자동으로 푸시함


class RestPost:
    @staticmethod
    def insert_vehicle(token):
        # Insert node, Selected AMR
        insert_node = request.form['node']
        amr = request.form['vehicle']
        print(request.form)

        try:
            uri_insert_amr = 'http://127.0.0.1:8081/wms/rest/vehicles/' + amr + '/command?&sessiontoken=' + token
            # %20 is blank
            data = {
                "command": {
                    "name": "insert",
                    "args": {
                        "nodeId": str(insert_node)
                    }
                }
            }

            # from Ant, POST response
            res_raw = requests.post(uri_insert_amr, data=json.dumps(data))
            print(res_raw.content)

            res = str(res_raw)
            if res != '<Response [200]>':
                return "Internal ANT Server Unavailable [500]"

            # post response from ANT(가 돼야함)
            # if request.form['vehicle'] != 'Vehicle%201':
            #     print(request.form['vehicle'])
            #
            #     if request.form['vehicle'] == '1':
            #         return 'Vehicle not found'
            #     elif request.form['vehicle'] == '3':
            #         return 'Vehicle is not ready for a new command'
            #     else:
            #         return 'Vehicle Error'
            print(request.form['vehicle']) # vehicle 이름체크용 임시

            return redirect(url_for('vehicle'))
        except Exception as err:
            return err

        # console print:
        # 1:

    @staticmethod
    def new_mission(token, msn_type, submit_type, start, stop):
        if token == '1':
            print('Logging in')
            return redirect(url_for('login', link='2'))

        if submit_type == 'delete':
            return redirect(url_for('new_mission'))

        # if submit_type == 'create':
        print(request.form)
        print(start + ", " + stop)

        try:
            uri_new_mission = 'http://127.0.0.1:8081/wms/rest/missions?&sessiontoken=' + token
            data = {
                "missionrequest": {
                    "requestor": "admin",
                    "missiontype": str(msn_type),
                    "fromnode": start,
                    "tonode": stop,
                    "cardinality": "1",
                    "priority": 2,

                    "parameters": {
                        "value": {
                            "payload": "Default payload"
                        },
                        "desc": "Mission extension",
                        "type": "org.json.JSONObject",
                        "name": "parameters"
                    }
                }
            }

            res_raw = requests.post(uri_new_mission, data=json.dumps(data))
            print(res_raw.content)

            return redirect(url_for('new_mission'))
        except Exception as err:
            return err

        # console print:
        # 1: post 내용
        # 2: fromNode, toNode request 결과
        # 3: request 결과

