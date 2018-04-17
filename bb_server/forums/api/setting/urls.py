#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-20 22:15:58 (CST)
# Last Update:星期五 2017-11-10 10:57:39 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint
from .views import ProfileView, ChangePasswordView, PrivacyView, BabelView, ChangePhoneView, ChangeUsernameView

site = Blueprint('setting', __name__, url_prefix='/api/setting')
setting_view = ProfileView.as_view('setting')
password_view = ChangePasswordView.as_view('password')
phone_view = ChangePhoneView.as_view('phone')
username_view = ChangeUsernameView.as_view('username')
privacy_view = PrivacyView.as_view('privacy')
babel_view = BabelView.as_view('babel')

site.add_url_rule('', view_func=setting_view)
site.add_url_rule('/profile', view_func=setting_view)
site.add_url_rule('/password', view_func=password_view)
site.add_url_rule('/phone', view_func=phone_view)
site.add_url_rule('/username', view_func=username_view)
site.add_url_rule('/privacy', view_func=privacy_view)
site.add_url_rule('/babel', view_func=babel_view)


def init_app(app):
    app.register_blueprint(site)
