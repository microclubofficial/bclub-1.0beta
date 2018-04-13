#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-20 22:16:04 (CST)
# Last Update:星期三 2017-5-10 16:35:45 (CST)
#          By:
# Description:
# **************************************************************************
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, logout_user
from forums.api.forms import (ProfileForm, PasswordForm, PrivacyForm,
                              AvatarForm, BabelForm)
from forums.common.views import IsConfirmedMethodView as MethodView
from flask_auth.form import form_validate
from flask_auth.auth.views import check_phone
from forums.func import get_json
from forums.api.user.models import User

def error_callback(url):
    return lambda: redirect(url_for(url))


class ProfileView(MethodView):
    def get(self):
        user = request.user
        form = ProfileForm()
        avatarform = AvatarForm()
        info = user.info
        form.introduce.data = info.introduce
        form.school.data = info.school
        form.word.data = info.word
        data = {'form': form, 'avatarform': avatarform}
        return render_template('setting/setting.html', **data)

    @form_validate(ProfileForm, error=error_callback('setting.setting'), f='')
    def post(self):
        form = ProfileForm()
        info = current_user.info
        info.introduce = form.introduce.data
        info.school = form.school.data
        info.word = form.word.data
        info.save()
        return redirect(url_for('setting.setting'))


class ChangePasswordView(MethodView):
    def get(self):
        form = PasswordForm()
        data = {'form': form}
        return render_template('setting/password.html', **data)

    @form_validate(
        PasswordForm, error=error_callback('setting.password'), f='')
    def post(self):
        user = request.user
        form = PasswordForm()
        if user.check_password(form.old_password.data):
            user.set_password(form.new_password.data)
            user.save()
            logout_user()
            return get_json(1, '修改密码成功，请重新登录', {})
        return get_json(0, '原密码错误', {})

class ChangePhoneView(MethodView):
    def post(self):
        user = request.user
        post_data = request.json
        phone = post_data['phone']
        captcha = post_data['captcha']
        if User.query.filter_by(phone = phone).exists():
            msg = '手机已被注册'
            return get_json(0, msg, {})
        if not check_phone(phone, captcha):
            return get_json(0, '验证码错误', {})
        user.phone = phone
        user.save()
        return get_json(1, '手机号已更换', {})

class ChangeUsernameView(MethodView):
    def post(self):
        user = request.user
        post_data = request.json
        username = post_data['username']
        if User.query.filter_by(username = username).exists():
            msg = '用户名已存在'
            return get_json(0, msg, {})
        user.username = username
        user.save()
        return get_json(1, '用户名已更换', {})        

class PrivacyView(MethodView):
    def get(self):
        user = request.user
        setting = user.setting
        form = PrivacyForm()
        form.online_status.data = setting.online_status
        form.topic_list.data = setting.topic_list
        form.rep_list.data = setting.rep_list
        form.ntb_list.data = setting.ntb_list
        form.collect_list.data = setting.collect_list
        return render_template('setting/privacy.html', form=form)

    @form_validate(PrivacyForm, error=error_callback('setting.privacy'), f='')
    def post(self):
        user = request.user
        form = PrivacyForm()
        setting = user.setting
        setting.online_status = form.online_status.data
        setting.topic_list = form.topic_list.data
        setting.rep_list = form.rep_list.data
        setting.ntb_list = form.ntb_list.data
        setting.collect_list = form.collect_list.data
        setting.save()
        return redirect(url_for('setting.privacy'))


class BabelView(MethodView):
    def get(self):
        user = request.user
        setting = user.setting
        form = BabelForm()
        form.timezone.data = setting.timezone
        form.locale.data = setting.locale
        return render_template('setting/babel.html', form=form)

    @form_validate(BabelForm, error=error_callback('setting.babel'), f='')
    def post(self):
        user = request.user
        setting = user.setting
        form = BabelForm()
        setting.timezone = form.timezone.data
        setting.locale = form.locale.data
        setting.save()
        return redirect(url_for('setting.babel'))
