#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: __init__.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-10-28 10:02:51 (CST)
# Last Update:星期三 2017-12-13 16:13:45 (CST)
#          By:
# Description:
# **************************************************************************
from flask_admin import Admin
from forums.admin import bar, user, topic, message, permission

from flask_admin import expose, AdminIndexView
from forums.api.user.models import User
from flask import redirect, url_for, request
from flask_login import current_user
from forums.func import get_json
'''
class MyAdminIndexView(AdminIndexView):
    
    @expose('/admin')
    def index(self):
        if not current_user.is_authenticated():
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/admin/login', methods=('GET', 'POST'))
    def login_view(self):
        post_data = request.data
        username = post_data.get('username')
        password = post_data.get('password')
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return get_json(0, '用户名或密码错误', {})
        user.login()
        return redirect(url_for('.index'))

admin1 = Admin(index_view=AdminIndexView())'''
admin = Admin(name='Bclub', template_mode='bootstrap3')

def init_app(app):
    admin.init_app(app)
    bar.init_admin(admin)
    user.init_admin(admin)
    topic.init_admin(admin)
    #message.init_admin(admin)
    #permission.init_admin(admin)
