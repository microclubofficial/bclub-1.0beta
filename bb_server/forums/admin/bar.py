#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: forums.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-17 13:12:23 (CST)
# Last Update:星期五 2017-11-10 11:04:16 (CST)
#          By:
# Description:
# **************************************************************************
from .views import BaseView
from forums.extension import db
from forums.api.forums.models import Board
from forums.api.bar.models import Bar,Questions
from forums.api.tag.models import Tags


class BarView(BaseView):
    column_searchable_list = ('title', 'subtitle', 'author.username')   #搜索条件
    column_filters = ['title', 'subtitle', 'author.username']
    pass


class QuestionView(BaseView):
    column_searchable_list = ('title', 'content', 'author.username')   #搜索条件
    column_filters = ['author.username', 'title']    #筛选元素
    column_exclude_list = ['content', 'is_bar']                 #排除
    column_editable_list = ['title', 'content_type', 'bar']  #可点击
    column_default_sort = 'created_at'  #按时间排序
    column_formatters = dict(           #列表视图列格式化程序字典
        content=lambda v, c, m, p: m.content[:100] + '...',
        content_type=lambda v, c, m, p: m.get_choice_display('content_type', 'CONTENT_TYPE')
    )
    form_choices = {'content_type': Questions.CONTENT_TYPE}    #在列表视图中将选项映射到列
    form_widget_args = {'content': {'rows': 10}}    #表单控件渲染参数字典。使用它可以自定义如何在不使用自定义模板的情况下呈现小部件
    #form_excluded_columns = ('replies', 'collects', 'followers')    #排除的表单字段名称的集合。


def init_admin(admin):
    admin.add_view(
        BarView(
            Bar,
            db.session,
            name='管理吧',
            endpoint='admin_bar',
            category='管理论坛'))
    admin.add_view(
        QuestionView(
            Questions,
            db.session,
            name='管理问题',
            endpoint='admin_tag',
            category='管理论坛'))
