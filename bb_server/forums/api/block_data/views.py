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
        data['global_market_rate'] = ('%.2f%%' % (data['marketCap']/total_market_cap_usd * 100))
        data['Circulation_rate'] = ('%.2f%%' % (data['available_supply']/data['supple'] * 100))
        data['kline'] = kline.json()['data']
        data['picture'] = 'https://blockchains.oss-cn-shanghai.aliyuncs.com/static/coinInfo/%s.png'%(token)
        return get_json(1, 'success', data)

class B_List(MethodView):
    def get(self, page, limit):
        offset = (int(page)-1)*int(limit)
        blist = requests.get('https://api.tokenclub.com/v2/ticker/summary?type=0&offset=%s&limit=%s'%(offset, limit))
        blist = blist.json()['data']
        for i in blist['summaryList']:
            i['picture'] = 'https://blockchains.oss-cn-shanghai.aliyuncs.com/static/coinInfo/%s.png'%(i['id'])
        print(blist,999999999999999999999999999999999999999999999999999)
        return get_json(1, 'success', blist)
