from flask import jsonify, current_app, request
from sqlalchemy import inspect
from flask_login import current_user
from flask_babel import gettext as _
import datetime
import json

#from forums.api.collect.models import Collect


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
    diff = now - update_time
    if int(diff.seconds)<=60:
        if int(diff.seconds) == 1:
            return str(diff.seconds)+_(' second')
        return str(diff.seconds)+_(' seconds')
    elif int(diff.seconds)<=3600:
        if int(diff.seconds//60) == 1:
            return str(int(diff.seconds//60))+_(' minute')
        return str(int(diff.seconds//60))+_(' minutes')
    elif int(diff.days)==0:
        if int(diff.seconds//3600) == 1:
            return str(int(diff.seconds//3600))+_(' hour')
        return str(int(diff.seconds//3600))+_(' hours')
    elif int(diff.days)<=7:
        if int(diff.days) == 1:
            return str(int(diff.days))+_(' day')
        return str(int(diff.days))+_(' days')
    return str(update_time)

def FindAndCount(Sql,**kwargs):
    count = Sql.query.filter_by(**kwargs).count()
    return count

def Avatar(data, user):
    if user.avatar:
        data['avatar'] = user.avatar
    else:
        data['avatar'] = '/api/{}/avatar'.format(user.username)
    return 

def Count(Sql, data=False):
    if current_user.is_authenticated:
        if request.user.id in json.loads(Sql):
            data = True
    return len(json.loads(Sql)), data

'''def collect_bool(topicid):
    if current_user.is_authenticated: 
        topic_id = Collect.query.with_entities(Collect.topic_id).filter_by(author_id = request.user.id).first()
        if not topic_id:
            return False
        if topicid in json.loads(topic_id[0]):
            return True
        else:
            return False
    return False'''

def json_loads(data, list):
    for i in list:
        try:
            data[i] = json.loads(data[i])
        except:
            data[i] = data[i]
    return

def bool_delete(user, bool_alter = False):
    if current_user.is_authenticated:
        if request.user == user:
            bool_alter = True
    return bool_alter
