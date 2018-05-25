#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-17 13:15:10 (CST)
# Last Update:星期日 2018-01-07 22:06:09 (CST)
#          By:
# Description:
# **************************************************************************
from flask import abort, request
from flask_admin.contrib.sqla import ModelView
from flask_wtf import Form
from forums.permission import super_permission
from flask_login import current_user
from forums.func import object_as_dict
from forums.api.user.models import User

from forums.extension import redis_data

class BaseForm(Form):
    def __init__(self, formdata=None, obj=None, prefix=u'', **kwargs):
        self._obj = obj
        super(BaseForm, self).__init__(
            formdata=formdata, obj=obj, prefix=prefix, **kwargs)


class BaseView(ModelView):

    page_size = 10
    can_view_details = True
    form_base_class = BaseForm

    def is_accessible(self):
        uuid = request.cookies.get('uuid')
        username = redis_data.get(uuid)
        #username = session.get('admin_username', None)
        if User.query.filter_by(username=username).exists():
            user = User.query.filter_by(username=username).first()
            return user.is_superuser
        return False
        
    def inaccessible_callback(self, name, **kwargs):
        abort(404)
