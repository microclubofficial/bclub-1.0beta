#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ********************************************************************************
# Copyright © 2018 jianglin
# File Name: maple.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2018-02-11 14:56:08 (CST)
# Last Update: 星期日 2018-02-11 15:26:53 (CST)
#          By:
# Description:
# ********************************************************************************
from flask_auth.bootstrap import Bootstrap
from flask_auth.captcha import Captcha
from flask_auth.error import Error
from flask_auth.app import App
from flask_auth.json import CustomJSONEncoder
from flask_auth.middleware import Middleware
from flask_auth.log import Logging

bootstrap = Bootstrap(
    css=('styles/monokai.css', 'styles/mine.css'),
    js=('styles/upload.js', 'styles/forums.js', 'styles/following.js',
        'styles/topic.js'),
    use_auth=True)


def init_app(app):
    bootstrap.init_app(app)
    Captcha(app)
    Error(app)
    App(app, json=CustomJSONEncoder)
    Middleware(app)
    Logging(app)
