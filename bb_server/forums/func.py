from flask import jsonify
from sqlalchemy import inspect
import datetime

def get_json(errorcode,msg,data):
    data_json={
        'resultcode':errorcode,
        'message':msg,
        'data':
            data
    }
    return jsonify(data_json)

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}

def time_diff(update_time):
    now = datetime.datetime.now()
    time_diff = now - update_time
    if int(time_diff.seconds)<=60:
        return str(time_diff.seconds)+'s'
    elif int(time_diff.seconds)<=3600:
        return str(int(time_diff.seconds//60))+'min'
    elif int(time_diff.days)==0:
        return str(int(time_diff.seconds//3600))+'hour'
    elif int(time_diff.days)<=7:
        return str(int(time_diff.days))+'day'
    return update_time
