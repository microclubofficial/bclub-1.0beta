from flask import jsonify
from flask.views import MethodView
import requests

class B_Price(MethodView):
    def get(self):
        ori=requests.get('https://data.block.cc/api/v1/price?symbol=BTC')
        return jsonify(ori.text)