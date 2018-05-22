from flask.views import MethodView
from flask_babel import gettext as _
from forums.func import get_json, object_as_dict, Avatar
from forums.api.topic.models import Topic, Reply
from sqlalchemy import func
from forums.api.user.models import User
import math
import json

per_page = 5

class SideInfluence(MethodView):
    def get(self, page):
        start = (page-1)*per_page
        influence = Reply.query.with_entities(Reply.author_id,func.count(Reply.author_id)).group_by(
            'author_id').order_by(-func.count('author_id')).limit(per_page).offset(start)
        data=[]
        count = Reply.query.with_entities(Reply.author_id).group_by('author_id').all()
        sum_count = len(count)
        page_count = int(math.ceil(sum_count/per_page))
        for i in influence:
            reply = {}
            user = User.query.filter_by(id = i[0]).first()
            Avatar(reply, user)
            reply['username'] = user.username
            reply['reply_count'] = i[1]
            data.append(reply)
        influence_data = {'reply':data, 'sum_count': sum_count, 'page_count': page_count}
        msg = _('influence')
        return get_json(1, msg, influence_data)

class SideAnalyst(MethodView):
    def get(self, page):
        start = (page-1)*per_page
        is_goodlist = Topic.query.with_entities(Topic.is_good, Topic.author_id).filter_by().all()
        datalist = {}
        for i in is_goodlist:
            i = list(i)
            i[0] = json.loads(i[0])
            if i[1] in datalist:
                datalist[i[1]] = datalist[i[1]] + len(i[0])
            else:
                datalist[i[1]] = len(i[0])
        datalist = sorted(datalist.items(), key=lambda item:item[1], reverse=True)
        sum_count = len(datalist)
        page_count = int(math.ceil(sum_count/per_page))
        data = []
        for i in datalist[start:(start+per_page)]:
            thumb = {}
            user = User.query.filter_by(id = i[0]).first()
            Avatar(thumb, user)
            thumb['username'] = user.username
            thumb['sum_is_good'] = i[1]
            data.append(thumb)
        analyst_data = {'analyst':data, 'sum_count': sum_count, 'page_count': page_count}
        msg = _('analyst')
        return get_json(1, msg, analyst_data)
