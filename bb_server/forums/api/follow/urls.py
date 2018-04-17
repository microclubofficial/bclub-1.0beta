#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-22 21:49:08 (CST)
# Last Update:星期五 2017-11-10 10:57:11 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint
from .views import (FollowingTagsView, FollowingUsersView, FollowingTokenView)

site = Blueprint('follow', __name__, url_prefix='/api/following')

token_view = FollowingTokenView.as_view('topic')
tag_view = FollowingTokenView.as_view('tag')
user_view = FollowingUsersView.as_view('user')


site.add_url_rule('/<token>', view_func=token_view)
site.add_url_rule('/token', view_func=token_view)
site.add_url_rule('/tags', view_func=tag_view)
site.add_url_rule('/users', view_func=user_view)


def init_app(app):
    app.register_blueprint(site)
