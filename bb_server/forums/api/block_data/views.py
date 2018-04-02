from flask import jsonify
from flask.views import MethodView
from forums.func import get_json
import requests


class B_Price(MethodView):
    def get(self, token):
        ori=requests.get('https://data.block.cc/api/v1/price?symbol=' + token)
        return get_json(1, token + '的价格', ori.json()['data'][0])

class B_Histery(MethodView):
    def get(self, token, limit):
        ori=requests.get('https://data.block.cc/api/v1/price/history?symbol=%s&limit=%s'%(token, limit))
        return get_json(1, token + '历史的价格', ori.json()['data'])
