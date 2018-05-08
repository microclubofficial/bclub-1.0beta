#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-15 22:08:06 (CST)
# Last Update:星期日 2017-4-2 11:51:33 (CST)
#          By:
# Description:
# **************************************************************************
from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required
from forums.api.forums.models import Board
from forums.api.tag.models import Tags
from forums.api.topic.models import Topic, Reply
from forums.api.collect.models import Collect
from forums.common.utils import gen_filter_dict, gen_order_by
from forums.common.views import BaseMethodView as MethodView
from forums.func import get_json, object_as_dict, Avatar, Count, FindAndCount, time_diff
from datetime import datetime
import math

from .models import User

per_page = 5

class UserListView(MethodView):
    @login_required
    def get(self):
        query_dict = request.data
        #page, number = self.page_info
        keys = ['username']
        order_by = gen_order_by(query_dict, keys)
        filter_dict = gen_filter_dict(query_dict, keys)
        users = User.query.filter_by(
            **filter_dict).order_by(*order_by).all()#.paginate(page, number, True)
        data = []
        for i in users:
            data.append(object_as_dict(i))
        return get_json(1, '所有用户', data)


class UserTopicView(MethodView):
    def get(self, username, page):
        start = (page-1)*per_page
        query_dict = request.data
        user = User.query.filter_by(username=username).first_or_404()
        keys = ['title']
        order_by = gen_order_by(query_dict, keys)
        filter_dict = gen_filter_dict(query_dict, keys)
        filter_dict.update(author_id=user.id)
        #elif request.path.endswith('top'):
        #    filter_dict.update(is_bad=True)
        #    title = _('bad Topics')
        topics = Topic.query.filter_by(
            **filter_dict).order_by(*order_by).limit(per_page).offset(start)
        topic_count = FindAndCount(Topic, **filter_dict)
        page_count = int(math.ceil(topic_count/per_page))
        topic = []
        for i in topics:
            reply_count = FindAndCount(Reply, topic_id = i.id)
            diff_time = time_diff(i.updated_at)
            i.created_at = str(i.created_at)
            i.updated_at = str(i.updated_at)
            topics_data = object_as_dict(i)
            topics_data['author'] = user.username
            topics_data['diff_time'] = diff_time
            topics_data['replies_count'] = reply_count
            topics_data['is_good'], topics_data['is_good_bool'] = Count(i.is_good)
            topics_data['is_bad'], topics_data['is_bad_bool'] = Count(i.is_bad)
            Avatar(topics_data, user)
            topic.append(topics_data)
        user_data = {}
        Avatar(user_data, user)
        user_data['username'] = user.username
        user = object_as_dict(user)
        if user.pop('is_confirmed'):
            user_data['is_confirm'] = '邮箱未认证'
        if user.pop('is_superuser'):
            user_data['Authority'] = '管理员'
        else:
            user_data['Authority'] = '普通用户'
        data = {'topics': topic, 'topic_count':topic_count, 'page_count':page_count, 'user_data': user_data}
        return get_json(1, '文章列表', data)


class UserReplyListView(MethodView):
    def get(self, username, page):
        start = (page-1)*per_page
        query_dict = request.data
        user = User.query.filter_by(username=username).first_or_404()
        keys = ['title']
        order_by = gen_order_by(query_dict, keys)
        filter_dict = gen_filter_dict(query_dict, keys)
        filter_dict.update(author_id=user.id)
        replies = Reply.query.filter_by(
            **filter_dict).order_by('-id').limit(per_page).offset(start)
        sum_count = FindAndCount(Reply, **filter_dict)
        page_count = int(math.ceil(sum_count/per_page))
        topics = []
        for i in replies:
            topic = i.topic
            #topic = Topic.query.filter_by(id=i.topic_id).first()
            if topic.id not in [i['id'] for i in topics]:
                topic_user = topic.author
                #topic_user = User.query.filter_by(id = topic.author_id).first()
                reply_count = FindAndCount(Reply, topic_id = topic.id)
                diff_time = time_diff(topic.updated_at)
                topics_data = object_as_dict(topic)
                topics_data['created_at'] = str(topics_data['created_at'])
                topics_data['updated_at'] = str(topics_data['created_at'])
                topics_data['author'] = topic_user.username
                topics_data['diff_time'] = diff_time
                topics_data['replies_count'] = reply_count
                topics_data['is_good'], topics_data['is_good_bool'] = Count(i.is_good)
                topics_data['is_bad'], topics_data['is_bad_bool'] = Count(i.is_bad)
                Avatar(topics_data, topic_user)
                topics.append(topics_data)
        data = {'topics': topics, 'sum_count':sum_count, 'page_count':page_count}
        return get_json(1, '评论的文章列表', data)


class UserFollowerListView(MethodView):
    @login_required
    def get(self, username):
        user = User.query.filter_by(username=username).first_or_404()
        page, number = self.page_info
        followers = user.followers.paginate(page, number, True)
        data = {'followers': followers, 'user': user}
        return render_template('user/followers.html', **data)

class UserView(MethodView):
    def get(self, username):
        user = User.query.filter_by(username=username).first_or_404()
        id = user.id
        user.last_login = str(user.last_login)
        user.register_time = str(user.register_time)
        user_data = object_as_dict(user)
        Avatar(user_data, user)
        keys = ['password']
        for i in keys:
            user_data.pop(i)
        if user_data.pop('is_confirmed'):
            user_data['is_confirm'] = '邮箱未认证'
        if user_data.pop('is_superuser'):
            user_data['Authority'] = '管理员'
        else:
            user_data['Authority'] = '普通用户'
        if not current_user.is_active:
            user_data['_user'] = '游客浏览'
        elif request.user.id == id:
            user_data['_user'] = '本人'
        else:
            user_data['_user'] = '非本人'
        return get_json(1, '个人资料', user_data)
        