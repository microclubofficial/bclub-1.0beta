#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: topic.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-17 13:01:43 (CST)
# Last Update:星期五 2017-11-10 11:06:21 (CST)
#          By:
# Description:
# **************************************************************************
from forums.extension import db
from forums.api.topic.models import Topic, Reply
from forums.api.collect.models import Collect
from .views import BaseView


class TopicView(BaseView):
    column_searchable_list = ('title', 'content', 'token', 'author.username')   #搜索条件
    column_filters = ['author.username', 'title', 'token']    #筛选元素
    column_exclude_list = ['content']                 #排除
    column_editable_list = ['title', 'content_type']  #可点击
    column_default_sort = ('created_at', True)  #按时间降序排序
    column_formatters = dict(           #列表视图列格式化程序字典
        content=lambda v, c, m, p: m.content[:100] + '...',
        content_type=lambda v, c, m, p: m.get_choice_display('content_type', 'CONTENT_TYPE')
    )
    form_choices = {'content_type': Topic.CONTENT_TYPE}    #在列表视图中将选项映射到列
    #form_widget_args = {'content': {'rows': 10}}    #表单控件渲染参数字典。使用它可以自定义如何在不使用自定义模板的情况下呈现小部件
    form_excluded_columns = ('replies', 'collects', 'followers', 'topic', 'tags', 'board')    #排除的表单字段名称的集合。
    #form_ajax_refs = {'tags': {'fields': ('name', ), 'page_size': 10}}  #使用AJAX进行外键模型加载。


class CollectView(BaseView):
    pass


class ReplyView(BaseView):
    column_searchable_list = ['topic.title', 'content']
    column_filters = ['author.username', 'created_at']
    column_default_sort = ('created_at', True)
    #form_excluded_columns = ['likers']
    form_widget_args = {'content': {'rows': 10}}
    form_excluded_columns = ('likers')

def init_admin(admin):
    admin.add_view(
        TopicView(
            Topic,
            db.session,
            name='管理文章',
            endpoint='admin_topic',
            category='管理主题'))
    admin.add_view(
        CollectView(
            Collect,
            db.session,
            name='管理收藏',
            endpoint='admin_collect',
            category='管理主题'))
    admin.add_view(
        ReplyView(
            Reply,
            db.session,
            name='管理评论',
            endpoint='admin_reply',
            category='管理主题'))
