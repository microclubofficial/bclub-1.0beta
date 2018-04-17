#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-03-28 16:15:16 (CST)
# Last Update:星期五 2017-11-10 10:57:01 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint
from .views import CollectView, AddToCollectView

site = Blueprint('collect', __name__, url_prefix='/api')

site.add_url_rule('/collectlist/<int:page>', view_func=CollectView.as_view('list'))
site.add_url_rule(
    '/collect/<int:topicId>', view_func=CollectView.as_view('collect'))
site.add_url_rule(
    '/topic/<int:topicId>/collect',
    view_func=AddToCollectView.as_view('add_to_collect'))

def init_app(app):
    app.register_blueprint(site)
