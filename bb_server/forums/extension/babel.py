#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ********************************************************************************
# Copyright © 2018 jianglin
# File Name: babel.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2018-02-11 14:52:25 (CST)
# Last Update: 星期日 2018-02-11 15:31:25 (CST)
#          By:
# Description:
# ********************************************************************************
from flask import request, g, current_app
from flask_babel import Babel

babel = Babel()

@babel.localeselector
def get_locale():
    if request.path.startswith('/admin'):
        return 'zh'
    #user = getattr(g, 'user', None)
    lang = request.cookies.get('language')
    if lang:
        return lang
    #if user is not None:  
    return request.accept_languages.best_match(current_app.config['LANGUAGES']
                                               .keys())

@babel.timezoneselector
def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone

def init_app(app):
    babel.init_app(app)
