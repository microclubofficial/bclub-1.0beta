from flask import jsonify, current_app, request
from sqlalchemy import inspect
from flask_login import current_user
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
        return str(diff.seconds)+'秒'
    elif int(diff.seconds)<=3600:
        return str(int(diff.seconds//60))+'分钟'
    elif int(diff.days)==0:
        return str(int(diff.seconds//3600))+'小时'
    elif int(diff.days)<=7:
        return str(int(diff.days))+'天'
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