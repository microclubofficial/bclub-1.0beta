#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-03-28 16:15:08 (CST)
# Last Update:星期三 2017-5-10 16:35:10 (CST)
#          By:
# Description:
# **************************************************************************
from flask import redirect, render_template, request, url_for
from flask_babelex import gettext as _
from flask_login import current_user

from flask_auth.form import form_validate
from flask_auth.response import HTTPResponse
from forums.api.forms import (CollectForm, ReplyForm, TopicForm,
                              collect_error_callback, error_callback,
                              form_board)
from forums.api.forums.models import Board
from forums.api.tag.models import Tags
from forums.api.topic.models import Topic, Reply
from forums.api.user.models import User
from forums.common.serializer import Serializer
from forums.common.utils import gen_filter_dict, gen_order_by
from forums.common.views import IsAuthMethodView as MethodView
from forums.api.message.models import MessageClient
from forums.func import get_json, FindAndCount, Count, object_as_dict, Avatar, time_diff
import json
import math

from .models import Collect

per_page = 5
'''
class CollectListView(MethodView):
    def get(self):
        query_dict = request.data
        user = request.user
        form = CollectForm()
        page, number = self.page_info
        keys = ['name']
        order_by = gen_order_by(query_dict, keys)
        filter_dict = gen_filter_dict(query_dict, keys)
        filter_dict.update(author_id=user.id)
        collects = Collect.query.filter_by(
            **filter_dict).order_by(*order_by).paginate(page, number, True)
        data = {'title': 'Collect', 'collects': collects, 'form': form}
        return render_template('collect/collect_list.html', **data)

    @form_validate(CollectForm, error=collect_error_callback, f='')
    def post(self):
        user = request.user
        form = CollectForm()
        name = form.name.data
        description = form.description.data
        is_hidden = form.is_hidden.data
        is_hidden = True if is_hidden == 0 else False
        collect = Collect(
            name=name, description=description, is_hidden=is_hidden)
        collect.author = user
        collect.save()
        return redirect(url_for('collect.list'))


class CollectView(MethodView):
    def get(self, pk):
        user = request.user
        page, number = self.page_info
        collect = Collect.query.filter_by(
            id=pk, author_id=user.id).first_or_404()
        form = CollectForm()
        form.name.data = collect.name
        form.description.data = collect.description
        form.is_hidden.data = 0 if collect.is_hidden else 1
        topics = collect.topics.paginate(page, number, True)
        data = {'collect': collect, 'topics': topics, 'form': form}
        return render_template('collect/collect.html', **data)

    def put(self, pk):
        post_data = request.data
        collect = Collect.query.filter_by(id=pk).first_or_404()
        name = post_data.pop('name', None)
        description = post_data.pop('description', None)
        is_hidden = post_data.pop('is_hidden', None)
        if name is not None:
            collect.name = name
        if description is not None:
            collect.description = description
        if is_hidden is not None:
            collect.is_hidden = is_hidden
        collect.save()
        return HTTPResponse(HTTPResponse.NORMAL_STATUS).to_response()

    def delete(self, pk):
        collect = Collect.query.filter_by(id=pk).first_or_404
        collect.delete()
        return HTTPResponse(HTTPResponse.NORMAL_STATUS).to_response()
        '''

class AddToCollectView(MethodView):
    def post(self, topicId):
        user = request.user
        form = request.form.getlist('add-to-collect')
        topic = Topic.query.filter_by(id=topicId).first_or_404()
        for cid in form:
            '''This has a problem'''
            collect = Collect.query.filter_by(id=cid).first_or_404()
            if not Collect.query.filter_by(
                    topics__id=topic.id, author_id=user.id).exists():
                collect.topics.append(topic)
                collect.save()
            MessageClient.collect(topic)
        return redirect(url_for('topic.topic', topicId=topic.id))

    # def delete(self, topicId):
    #     user = request.user
    #     form = request.form.getlist('add-to-collect')
    #     topic = Topic.query.filter_by(id=topicId).first_or_404()
    #     for cid in form:
    #         '''This has a problem'''
    #         collect = Collect.query.filter_by(id=cid).first_or_404()
    #         if not Collect.query.filter_by(
    #                 topics__id=topic.id, author_id=user.id).exists():
    #             collect.topics.append(topic)
    #             collect.save()
    #     return redirect(url_for('topic.topic', topicId=topic.id))

class CollectView(MethodView):

    def get(self, page):
        start = (page-1)*per_page
        user = request.user
        collect = Collect.query.filter_by(author_id = user.id).first()
        if collect:
            topiclist = json.loads(collect.topic_id)
            sum_count = len(topiclist)
            page_count = int(math.ceil(sum_count/per_page))
            topics = []
            for i in topiclist[-start-1:-start-per_page-1:-1]:
                topic = Topic.query.filter_by(id=i).first()
                user = User.query.filter_by(id = topic.author_id).first()
                reply_count = FindAndCount(Reply, topic_id = topic.id)
                diff_time = time_diff(topic.updated_at)
                topics_data = object_as_dict(topic)
                topics_data['created_at'] = str(topics_data['created_at'])
                topics_data['updated_at'] = str(topics_data['created_at'])
                topics_data['author'] = user.username
                topics_data['diff_time'] = diff_time
                topics_data['replies_count'] = reply_count
                topics_data['is_good'], topics_data['is_good_bool'] = Count(topic.is_good)
                topics_data['is_bad'], topics_data['is_bad_bool'] = Count(topic.is_bad)
                #a, topics_data['collect_bool'] = Count(Collect.topic_id)
                Avatar(topics_data, user)
                topics.append(topics_data)
            data = {'topics': topics, 'sum_count':sum_count, 'page_count':page_count}
            return get_json(1, '收藏列表', data)
        return get_json(1, '收藏列表', {})

    def post(self, topicId):
        user = request.user
        if Collect.query.filter_by(author_id = user.id).exists():
            collect = Collect.query.filter_by(author_id = user.id).first()
            topiclist = json.loads(collect.topic_id)
            if topicId in topiclist:
                topiclist.remove(topicId)
                collect.topic_id = json.dumps(topiclist)
                collect.save()
                data={}
                data['collect_bool'] = False
                return get_json(1, '取消收藏成功', data)
            else:
                topiclist.append(topicId)
                collect.topic_id = json.dumps(topiclist)
        else:
            collect = Collect(author_id=user.id)
            collect.topic_id = json.dumps([topicId])
        collect.save()
        data={}
        data['collect_bool'] = True
        return get_json(1, '收藏成功', data)