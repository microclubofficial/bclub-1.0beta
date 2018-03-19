#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-21 21:56:41 (CST)
# Last Update:星期三 2017-5-10 16:35:21 (CST)
#          By:
# Description:
# **************************************************************************
from flask import (url_for, redirect, send_from_directory, current_app,
                   request, Response)
from flask.views import MethodView
from flask_login import login_required, current_user
from flask_auth.form import form_validate
from forums.api.forms import AvatarForm
from werkzeug.utils import secure_filename
from time import time
from random import randint
from PIL import Image
import os
from .models import Photo
from forums.func import get_json, object_as_dict

class AvatarView(MethodView):
    decorators = [login_required]

    @form_validate(
        AvatarForm, error=lambda: redirect(url_for('setting.setting')), f='')
    def post(self):
        print(11111111111111111111111111)
        form = AvatarForm()
        user = request.user
        file = request.files[form.avatar.name]
        filename = user.username + '-' + str(int(time())) + str(
            randint(1000, 9999))
        img = Image.open(file)
        size = 120, 120
        img.thumbnail(size, Image.ANTIALIAS)
        current_app.config.setdefault('AVATAR_FOLDER', os.path.join(
            current_app.static_folder, 'avatars'))
        avatar_path = current_app.config['AVATAR_FOLDER']
        avatar = os.path.join(avatar_path, filename + '.png')
        if not os.path.exists(avatar_path):
            os.makedirs(avatar_path)
        img.save(avatar)
        #img.close()
        info = user.info
        if info.avatar:
            ef = os.path.join(avatar_path, info.avatar)
            if os.path.exists(ef):
                os.remove(ef)
        # file.save(os.path.join(app.static_folder, filename + '.png'))
        info.avatar = filename + '.png'
        info.save()
        resp = Response(img, mimetype="image/jpeg")
        return resp
        #return redirect(url_for('setting.setting'))


class AvatarFileView(MethodView):
    def get(self, filename):
        current_app.config.setdefault('AVATAR_FOLDER', os.path.join(
            current_app.static_folder, 'avatars'))
        avatar_path = current_app.config['AVATAR_FOLDER']
        if not os.path.exists(os.path.join(avatar_path, filename)):
            filename = filename.split('-')[0]
            print(filename)
            return redirect(url_for('avatar', text=filename))
        return send_from_directory(avatar_path, filename)

class GetPhotoView(MethodView):
    def post(self, title_id):
        import pdb
        pdb.set_trace()
        form = AvatarForm()
        file = request.files[form.avatar.name]
        filename = title_id + '-' + str(int(time())) + str(
                randint(1000, 9999))
        img = Image.open(file)
        current_app.config.setdefault('AVATAR_FOLDER', os.path.join(
                current_app.static_folder, 'avatars'))
        photo_path = current_app.config['AVATAR_FOLDER']
        photo = os.path.join(photo_path, filename + '.png')
        if not os.path.exists(photo_path):
            os.makedirs(photo_path)
        photos = Photo(
            front_photo = file,
            photo_path = 'http://' + photo_path + filename + '.png')
        photos.save()
        img.save(photo)
        return get_json(1, '上传成功', object_as_dict(photos))
