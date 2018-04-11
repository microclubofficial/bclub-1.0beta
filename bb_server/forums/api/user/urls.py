#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-15 22:24:23 (CST)
# Last Update:星期五 2017-11-10 10:58:03 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint

from .views import (UserFollowerListView, UserListView, UserReplyListView,UserView)

site = Blueprint('user', __name__, url_prefix='/api/u')

user_list = UserListView.as_view('list')
user = UserView.as_view('user')
topics = UserView.as_view('topic')
replies = UserReplyListView.as_view('reply')
followers = UserFollowerListView.as_view('follower')

site.add_url_rule('', view_func=user_list)
site.add_url_rule('/<username>', view_func=user)
site.add_url_rule('/topics/<username>', view_func=topics)
site.add_url_rule('/replies/<username>', view_func=replies)
site.add_url_rule('/followers/<username>', view_func=followers)



def init_app(app):
    app.register_blueprint(site)
