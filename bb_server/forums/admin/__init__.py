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
from forums.admin import bar, user, topic, message, permission 
from flask_admin import expose, AdminIndexView, Admin
from forums.api.user.models import User
from flask import redirect, url_for, request, render_template
from flask_login import current_user
from forums.func import get_json
from flask.views import MethodView
from flask import Blueprint

class MyAdminIndexView(AdminIndexView):  
    @expose()
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('login.login'))
        user = request.user
        if user.is_superuser:
            return super(MyAdminIndexView, self).index()
        return redirect(url_for('login.login'))

class LoginView(MethodView):
    def get(self):
        return render_template('admin/login.html')

    def post(self):
        post_data = request.data
        username = post_data.get('username')
        password = post_data.get('password')
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return redirect('/admin/login')
        if not user.is_superuser:
            return redirect('/admin/login')
        user.login()
        return redirect('/admin')

admin = Admin(name='Bclub', index_view=MyAdminIndexView(name='导航栏', template='admin/index.html', url='/admin'))
#admin = Admin(name='Bclub', index_view=MyAdminIndexView(),template_mode='bootstrap3')
site = Blueprint('login', __name__)
site.add_url_rule('/admin/login', view_func=LoginView.as_view('login'))
def init_app(app):
    admin.init_app(app)
    bar.init_admin(admin)
    user.init_admin(admin)
    topic.init_admin(admin)
    #message.init_admin(admin)
    #permission.init_admin(admin)
    app.register_blueprint(site)

