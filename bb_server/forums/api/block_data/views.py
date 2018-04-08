from flask import jsonify
from flask.views import MethodView
from forums.func import get_json
import requests


class Currency_News(MethodView):
    def get(self, token):
        details = requests.get('https://block.cc/api/v1/coin/get?coin=%s'%(token))
        kline = requests.get('https://block.cc/api/v1/marketKline/%s'%(token))
        total_market_cap_usd = requests.get('https://block.cc/api/v1/getBaseTotalInfo')
        total_market_cap_usd = total_market_cap_usd.json()['data']["total_market_cap_usd"]
        details = details.json()['data']
        keys = ['id','name', 'symbol','price', 'volume_ex', "supple", "available_supply", 'marketCap', 'level', 'marketCap',
         'change1h', 'change7d', 'zhName', 'volume_level', 'low1d', 'high1d', 'CNY_RATE', 'BTC_RATE', 'ETH_RATE']
        data = {}
        for i in keys:
            data[i] = details[i]
        data['global_market _rate'] = ('%.2f%%' % (data['marketCap']/total_market_cap_usd * 100))
        print(data['global_market _rate'],99999999999999999999999999)
        data['Circulation_rate'] = data['available_supply']/data['supple']
        data['kline'] = kline.json()['data']
        data['picture'] = 'https://blockchains.oss-cn-shanghai.aliyuncs.com/static/coinInfo/%s.png'%(token)
        return get_json(1, 'success', data)
