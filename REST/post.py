from flask import Flask, render_template, redirect, url_for, request
import requests
import json

# Tip: Post하면 플라스크는 request를 자동생성하고 라우트핸들러가 처리되는 동안 각각의 함수나 메소드에서 request에 접근 가능.


class RestPost:
    def __init__(self):
        self.base_uri = 'http://127.0.0.1:8081/wms/'

    def route_action(self, token):
        act = request.form['action']

        if act == 'insert':
            return self.insert_vehicle(token)
        elif act == 'extract':
            return self.extract_vehicle(token)
        else:
            return 'Unknown button action'

    # 1대의 AMR 등록
    def insert_vehicle(self, token):
        try:
            insert_node = request.form['node']
            amr = request.form['vehicle']
            print(request.form)

            uri_insert_amr = self.base_uri + 'rest/vehicles/' + amr + '/command?&sessiontoken=' + token

            data = {
                "command": {
                    "name": "insert",
                    "args": {
                        "nodeId": str(insert_node)
                    }
                }
            }
            res_raw = requests.post(url=uri_insert_amr, data=json.dumps(data), timeout=20)
            print(res_raw.content)

            res = str(res_raw)
            if res != '<Response [200]>':
                return "Internal ANT Server Unavailable [500]"

            #     if request.form['vehicle'] == '1':
            #         return 'Vehicle not found'
            #     elif request.form['vehicle'] == '3':
            #         return 'Vehicle is not ready for a new command'
            #     else:
            #         return 'Vehicle Error'

            return redirect(url_for('vehicle'))
        except requests.Timeout:
            print("ANT 서버 타임아웃")

    def extract_vehicle(self, token):
        try:
            amr = request.form['vehicle']
            print(request.form)

            uri_extract_amr = self.base_uri + 'rest/vehicles/' + amr + '/command?&sessiontoken=' + token

            data = {
                "command": {
                    "name": "extract",
                    "args": {}
                }
            }
            res_raw = requests.post(url=uri_extract_amr, data=json.dumps(data), timeout=20)
            print(res_raw.content)

            res = str(res_raw)
            if res != '<Response [200]>':
                return "Internal ANT Server Unavailable [500]"

            return redirect(url_for('vehicle'))

        except requests.Timeout:
            print("ANT 서버 타임아웃")

    def new_mission(self, token):
        # 로그인이 안됐을때
        if token == '1':
            print('Logging in')
            return redirect(url_for('login', link='2'))

        # 미션 삭제일때
        if request.form['sb-type'] == 'delete':
            return redirect(url_for('new_mission'))

        # 미션 생성일때
        if request.method == 'POST' and "start" in request.form:
            start = request.form['start']
            stop = request.form['stop']
            msn_type = request.form['type']

            # 데이터 구조 example: ([('type', '7'), ('start', '100'), ('stop', '200'), ('btn-type', 'create')])
            # 데이터 타입: ImmutableMultiDict

            # if submit_type == 'create':
            print(request.form)
            print(start + ", " + stop)

            try:
                uri_new_mission = self.base_uri + 'rest/missions?&sessiontoken=' + token
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
                                "payload": "Default Payload"
                            },
                            "desc": "Mission extension",
                            "type": "org.json.JSONObject",
                            "name": "parameters"
                        }
                    }
                }

                res_raw = requests.post(uri_new_mission, data=json.dumps(data), timeout=20)
                print(res_raw.content)

                return redirect(url_for('new_mission'))
            except Exception as err:
                return "Error while mission creation"

            #
            # console print:
            # 1: post 내용
            # 2: fromNode, toNode request 결과
            # 3: request 결과

