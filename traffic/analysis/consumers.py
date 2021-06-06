# coding=utf-8
# chat/consumers.py
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json


class DriverConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        code = text_data_json["code"]
        data = text_data_json['msg']
        self.send(text_data=json.dumps(user_code_to_msg(code, data)))


# 301 交通堵塞
# 302 交通事故
# 303 天气预警
fakeSituation = [{"code": 301, "lon": 1, "lat": 2},
                 {"code": 302, "lon": 1, "lat": 2},
                 {"code": 303, "lon": 1, "lat": 2}]
loopIndex = 0


def checkSituation(lat, lon):
    global loopIndex
    situation = fakeSituation[loopIndex]
    loopIndex += 1
    if loopIndex == 3:
        loopIndex = 0
    code = situation["code"]
    if code == 303:
        return code
    accidentLat = situation["lat"]
    accidentLon = situation["lon"]
    if (accidentLat - lat) ** 2 + (accidentLon - lon) ** 2 <= 10:
        return code
    return 100


def user_code_to_msg(code, data):
    msg = {}
    if code == 100:
        msg['code'] = 100
        msg["msg"] = "当前路况无异常"
    elif code == 101:
        status = checkSituation(data['lat'], data['lon'])
        if status == 301:
            msg["msg"] = "前方道路堵塞，请注意避让"
        elif status == 302:
            msg["msg"] = "前方路段有重大事故，请注意避让"
        elif status == 303:
            msg["msg"] = "3小时内大雾预警，请注意行车安全"
        else:
            msg["msg"] = "当前路况无异常"
        msg["code"] = status
    return msg
