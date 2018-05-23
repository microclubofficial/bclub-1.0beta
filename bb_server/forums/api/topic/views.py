#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-15 22:07:39 (CST)
# Last Update: 星期日 2018-02-11 15:07:05 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Markup, redirect, render_template, request, url_for, current_app
from flask_babel import gettext as _
from flask_login import current_user, login_required

from flask_auth.form import form_validate
from flask_auth.response import HTTPResponse
from forums.api.forms import (CollectForm, ReplyForm, TopicForm,
                              collect_error_callback, error_callback,
                              form_board)
from forums.api.forums.models import Board
from forums.api.bar.models import Questions, Answers, Comments
from forums.api.tag.models import Tags
from forums.api.utils import gen_topic_filter, gen_topic_orderby
from forums.common.serializer import Serializer
from forums.common.utils import gen_filter_dict, gen_order_by
from flask.views import MethodView
from forums.common.views import IsAuthMethodView
from forums.jinja import safe_markdown
from .models import Reply, Topic
from .permissions import (like_permission, reply_list_permission,
                          reply_permission, topic_list_permission,
                          topic_permission, edit_permission, thumd_permission)
from forums.api.message.models import MessageClient
from forums.func import get_json, object_as_dict, time_diff, FindAndCount, Avatar, Count, json_loads, bool_delete
from forums.api.user.models import User
from forums.api.collect.models import Collect
from sqlalchemy import func
import math
import json
from forums.extension.babel import get_locale
import numpy as np

per_page = 5

def collect_bool(topicid):
    if current_user.is_authenticated: 
        topic_id = Collect.query.with_entities(Collect.topic_id).filter_by(author_id = request.user.id).first()
        if not topic_id:
            return False
        if topicid in json.loads(topic_id[0]):
            return True
        else:
            return False
    return False

class TopicAskView(IsAuthMethodView):
    def get(self):
        boardId = request.args.get('boardId', type=int)
        form = form_board()
        if boardId is not None:
            form.category.data = boardId
        data = {'title': _('Ask - '), 'form': form}
        return render_template('topic/ask.html', **data)

class TopicEditView(IsAuthMethodView):
    decorators = (edit_permission, )

    def get(self, topicId):
        topic = Topic.query.filter_by(id=topicId).first_or_404()
        form = form_board()
        form.title.data = topic.title
        form.category.data = topic.board_id
        form.tags.data = ','.join([tag.name for tag in topic.tags])
        form.content.data = topic.content
        data = {'title': _('Edit -'), 'form': form, 'topic': topic}
        return render_template('topic/edit.html', **data)

class TopicPreviewView(IsAuthMethodView):
    @login_required
    def post(self):
        post_data = request.data
        content_type = post_data.pop('content_type', None)
        content = post_data.pop('content', None)
        if content_type == Topic.CONTENT_TYPE_MARKDOWN:
            return safe_markdown(content)
        return content

class TopicListView(MethodView):
    decorators = (topic_list_permission, )

    def get(self, page, token=None):
        start = (page-1)*per_page
        query_dict = request.data
        keys = ['title']
        filter_dict = {}
        title = _('All Topics')     
        if 'token' in request.path:
            filter_dict['token'] = token
            title = _(token+'Topics')
        #elif request.path.endswith('top'):
        #    filter_dict.update(is_bad=True)
        #    title = _('bad Topics')
        topics = Topic.query.filter_by(**filter_dict).order_by('-id').limit(per_page).offset(start)
        topic_count = FindAndCount(Topic, **filter_dict)
        page_count = int(math.ceil(topic_count/per_page))
        topic = []
        for i in topics:
            user = i.author
            reply = Reply.query.filter_by(topic_id = i.id).order_by('-id').first()
            if reply:
                reply_user = reply.author.username
                reply_time = time_diff(reply.updated_at)
            else:
                reply_user = None
                reply_time = None
            reply_count = FindAndCount(Reply, topic_id = i.id)
            diff_time = time_diff(i.updated_at)
            i.created_at = str(i.created_at)
            i.updated_at = str(i.updated_at)
            collect = collect_bool(i.id)
            topics_data = object_as_dict(i)
            json_loads(topics_data, ['content', 'title'])
            topics_data['reply_time'] = reply_time
            topics_data['reply_user'] = reply_user
            topics_data['author'] = user.username
            topics_data['diff_time'] = diff_time
            topics_data['replies_count'] = reply_count
            topics_data['is_good'], topics_data['is_good_bool'] = Count(i.is_good)
            topics_data['is_bad'], topics_data['is_bad_bool'] = Count(i.is_bad)
            topics_data['collect_bool'] = collect
            topics_data['bool_delete'] = bool_delete(user)
            Avatar(topics_data, user)
            topic.append(topics_data)
        data = {'classification': title, 'topics': topic, 'topic_count':topic_count, 'page_count':page_count}
        msg = _('Topic List')
        return get_json(1, msg, data)

    def post(self):
        user = request.user
        post_data = request.data
        title = post_data.pop('title', None)
        content = post_data.pop('content', None)
        content_type = post_data.pop('content_type', 0)
        token = post_data.pop('token', None)
        zh_token = post_data.pop('tokenname', None)
        picture = post_data.pop('picture', None)
        topic = Topic(
            title=json.dumps(title),
            content=json.dumps(content),
            content_type=content_type,
            token = token,
            zh_token = zh_token,
            picture = picture)
        topic.author = user
        topic.save()
        topic = object_as_dict(topic)
        Avatar(topic, user)
        json_loads(topic, ['content', 'title'])
        topic['author'] = user.username
        topic['is_good'] = 0
        topic['is_bad'] = 0
        topic['diff_time'] = 0
        topic['bool_delete'] = bool_delete(user)
        msg = _('success')
        return get_json(1, msg, topic)

class TopicView(MethodView):
    decorators = (topic_permission, )
    
    def get(self, topicId, page):
        start = (page-1)*per_page
        query_dict = request.data
        topic = Topic.query.filter_by(id=topicId).first_or_404()
        diff_time = time_diff(topic.updated_at)
        topic.created_at = str(topic.created_at)
        topic.updated_at = str(topic.updated_at)
        reply = Reply.query.filter_by(topic_id = topicId).order_by(('-id')).limit(per_page).offset(start)
        reply_count = FindAndCount(Reply, topic_id = topicId)
        page_count = int(math.ceil(reply_count/per_page))
        replies = []
        for i in reply: 
            user = i.author
            diff_time = time_diff(i.updated_at)
            i.created_at = str(i.created_at)
            i.updated_at = str(i.updated_at)
            replies_data = object_as_dict(i)
            json_loads(replies_data, ['content', 'reference'])
            replies_data['author'] = user.username
            replies_data['diff_time'] = diff_time
            replies_data['is_good'], replies_data['is_good_bool'] = Count(i.is_good)
            replies_data['is_bad'], replies_data['is_bad_bool'] = Count(i.is_bad)
            replies_data['bool_delete'] = bool_delete(user)
            Avatar(replies_data, user)
            replies.append(replies_data)
        topic_user = topic.author   
        topic_data = object_as_dict(topic)
        json_loads(topic_data, ['content', 'title'])
        topic_data['author'] = topic_user.username
        topic_data['diff_time'] = diff_time
        topic_data['is_good'], topic_data['is_good_bool'] = Count(topic.is_good)
        topic_data['is_bad'], topic_data['is_bad_bool'] = Count(topic.is_bad)
        topic_data['collect_bool'] = collect_bool(topicId)
        topic_data['bool_delete'] = bool_delete(topic_user)
        Avatar(topic_data, topic_user)
        data = {
            'topic': topic_data,
            'replies': replies,
            'replies_count': reply_count,
            'page_count': page_count
        }
        msg = _('Topic Details')
        return get_json(1, msg, data)

    def post(self, topicId):
        user = request.user
        topic = Topic.query.filter_by(id=topicId).first()
        if user != topic.author:
            msg = _('You do not have permission to delete this article.')
            return get_json(0, msg, {})
        topic.delete()
        return get_json(1, _('success'), {})
        

class ReplyListView(MethodView):
    def get(self, topicId, page):
        start = (page-1)*per_page
        if 'early' in request.path:
            reply = Reply.query.filter_by(topic_id = topicId).order_by(('id')).limit(per_page).offset(start)
        elif 'good' in request.path:
            is_goodlist = Reply.query.with_entities(Reply.is_good, Reply.id).filter_by().all()
            a = []
            for i in is_goodlist:
                i = list(i)
                i[0] = len(json.loads(i[0]))
                a.append(i)
            b = []
            for i in a:
                b.append(i[0]) 
            c = np.array(b)
            d = np.argsort(c)[::-1][start:start+5]
            reply = []
            for i in d:
                _reply = Reply.query.filter_by(id = a[i][1]).first()
                reply.append(_reply)
            #reply = Reply.query.filter_by(topic_id = topicId).order_by(('-id')).limit(per_page).offset(start)
        else:
            reply = Reply.query.filter_by(topic_id = topicId).order_by(('-id')).limit(per_page).offset(start)
        reply_count = FindAndCount(Reply, topic_id = topicId)
        page_count = int(math.ceil(reply_count/per_page))
        replies = []
        for i in reply: 
            user = i.author
            #user = User.query.filter_by(id = i.author_id).first()
            diff_time = time_diff(i.updated_at)
            i.created_at = str(i.created_at)
            i.updated_at = str(i.updated_at)
            replies_data = object_as_dict(i)
            #replies_data['content'] = json.loads(replies_data['content'])
            json_loads(replies_data, ['content', 'reference'])
            replies_data['author'] = user.username
            replies_data['diff_time'] = diff_time
            replies_data['is_good'], replies_data['is_good_bool'] = Count(i.is_good)
            replies_data['is_bad'], replies_data['is_bad_bool'] = Count(i.is_bad)
            replies_data['bool_delete'] = bool_delete(user)
            Avatar(replies_data, user)
            replies.append(replies_data)
        data = {'page_count':page_count, 'reply_count':reply_count, 'replies':replies}
        msg = _('Replies Information')
        return get_json(1, msg, data)

    decorators = (reply_list_permission, )
    #@form_validate(ReplyForm, error=error_callback, f='')
    def post(self, topicId):
        #topic = Topic.query.filter_by(id=topicId).first_or_404()
        post_data = request.data
        user = request.user
        content = post_data.pop('content', None)
        reference = post_data.pop('replyContent', None)
        at_user = post_data.pop('author', None)
        reply = Reply(content=json.dumps(content), reference = json.dumps(reference), topic_id = topicId, at_user = at_user)
        #user = User.query.filter_by(id=1).first()
        reply.author_id = user.id
        reply.save()
        reply_count = FindAndCount(Reply, topic_id = topicId)
        reply.created_at = str(reply.created_at)
        reply.updated_at = str(reply.updated_at)
        replies_data = object_as_dict(reply)
        Avatar(replies_data, user)
        #replies_data['content'] = json.loads(replies_data['content'])
        json_loads(replies_data, ['content', 'reference'])
        replies_data['author'] = user.username
        replies_data['is_good'] = 0 
        replies_data['is_bad'] = 0
        replies_data['diff_time'] = 0
        replies_data['replies_count'] = reply_count
        replies_data['bool_delete'] = bool_delete(user)
        # noticetopicId
        #MessageClient.topic(reply)
        # count
        #topic.board.post_count = 1
        #reply.author.reply_count = 1Topic.query
        msg = _('success')
        return get_json(1, msg, replies_data)

class ReplyView(MethodView):
    decorators = (reply_permission, )

    def post(self, replyId):
        user = request.user
        reply = Reply.query.filter_by(id = replyId).first()
        if user != reply.author:
            msg = _('You do not have permission to delete this reply.')
            return get_json(0, msg, {})
        reply.delete()
        return get_json(1, _('success'), {})

class ThumbView(IsAuthMethodView):

    def get(self, id, thumb):
        user = request.user
        if 'topic' in request.path:
            session = Topic.query.filter_by(id = id).first()
        elif 'reply' in request.path:
            session = Reply.query.filter_by(id = id).first()
        elif 'question' in request.path:
            session = Questions.query.filter_by(id = id).first()
        elif 'answer' in request.path:
            session = Answers.query.filter_by(id = id).first()
        elif 'comment' in request.path:
            session = Comments.query.filter_by(id = id).first() 
        userlist_good = json.loads(session.is_good)
        userlist_bad = json.loads(session.is_bad)
        if thumb == 'up':
            if user.id in userlist_good:
                userlist_good.remove(user.id)
            elif user.id in userlist_bad:
                userlist_bad.remove(user.id)
                userlist_good.append(user.id)
            else:
                userlist_good.append(user.id)
        elif thumb == 'down':
            if user.id in userlist_bad:
                userlist_bad.remove(user.id)
            elif user.id in userlist_good:
                userlist_good.remove(user.id)
                userlist_bad.append(user.id)
            else:
                userlist_bad.append(user.id)
        session.is_good = json.dumps(userlist_good)
        session.is_bad = json.dumps(userlist_bad)
        session.save()
        data = {}
        data['is_good'], data['is_good_bool'] = Count(session.is_good)
        data['is_bad'], data['is_bad_bool'] = Count(session.is_bad)
        msg =_('success')
        return get_json(1, msg, data)

