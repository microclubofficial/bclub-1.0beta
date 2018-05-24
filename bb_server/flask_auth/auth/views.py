#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-07 14:01:14 (CST)
# Last Update:星期一 2018-01-08 11:21:43 (CST)
#          By:
# Description:
# **************************************************************************
from flask import flash, redirect, render_template, request, url_for, session
from flask_auth.response import HTTPResponse
from forums.func import get_json, object_as_dict, Avatar
from functools import wraps
from random import sample, randint
from string import ascii_letters, digits
from flask.views import MethodView
from flask_login import current_user, login_required
from flask_auth.serializer import Serializer
from flask_babel import gettext as _
from flask_auth.models import db
from forums.extension import redis_data
import requests

User = db.Model._decl_class_registry['User']


def guest_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        if current_user.is_authenticated:
            user = request.user
            data = {"username":user.username}
            Avatar(data, user)
            msg = _("You have login ,needn't login again")
            return get_json(0, msg, data)
        return func(*args, **kwargs)
    return decorator


def check_params(keys):
    def _check_params(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            post_data = request.json
            for key in keys:
                if not post_data.get(key):
                    
                    babel = {
                        'username': _("Username"),
                        'password': _("Password"),
                        'phone': _("Phone"),
                        'phonecaptcha': _("PhoneCaptcha"),
                        'captcha': _("Captcha"),
                        'confirm_password': _("Confirm_password"),
                    }
                    msg = _('The %(key)s is required', key=babel[key])
                    return get_json(0, msg, {}) 
            return func(*args, **kwargs)

        return decorator

    return _check_params

def check_captcha(phone, captcha):
    redis_captcha = redis_data.get(phone)
    if not redis_captcha:
        return False
    if redis_captcha != captcha:
        return False
    return True

def check_phone(phone):
    if User.query.filter_by(phone=phone).exists():
        return True
    return False

class LoginView(MethodView):
    decorators = [guest_required]

    @check_params(['username', 'password'])
    def post(self):
        post_data = request.json
        username = post_data['username']
        password = post_data['password']
        remember = post_data.pop('remember', False)
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            msg = _('Username or Password Error')
            return get_json(0, msg, {})
        captcha = post_data['captcha']
        session_captcha = session.pop('captcha', '00000')
        if captcha.lower() != session_captcha.lower():
            msg = _('The captcha is error')
            return get_json(0, msg, {})  
        user.login(remember)
        data = {"username":user.username}
        Avatar(data, user)
        msg = _('You have login')
        return get_json(1, msg, data)

class PhoneLoginView(MethodView):
    decorators = [guest_required]

    @check_params(['phone', 'phonecaptcha'])
    def post(self):
        post_data = request.json
        phone = post_data['phone']
        captcha = post_data['phonecaptcha']
        remember = post_data.pop('remember', False)
        user = User.query.filter_by(phone=phone).first()
        if not user:
            msg = _('The phone is error')
            return get_json(0, msg, {})
        if not check_captcha(phone, captcha):
            msg = _('The captcha is error')
            return get_json(0, msg, {})
        user.login(remember)
        data = {"username":user.username}
        Avatar(data, user)
        redis_data.delete(phone)
        msg = _('You have login')
        return get_json(1, msg, data)
        

class LogoutView(MethodView):
    decorators = [login_required]

    def post(self):
        current_user.logout()
        msg = _('You have logout')
        return get_json(1, msg, {})


class RegisterView(MethodView):
    def get(self):
        msg = _('register')
        return get_json(1, msg, {})

    @check_params(['username', 'password', 'confirm_password', 'phone', 'captcha'])
    def post(self):
        post_data = request.json
        username = post_data['username'] 
        password = post_data['password']
        confirm_password = post_data['confirm_password']    
        phone = post_data['phone']   
        captcha = post_data['captcha']
        if 'recommender_code' in post_data:
            recommender_code = post_data['recommender_code']
        else:
            recommender_code = None
        if check_phone(phone):
            msg = _('The phone has been registered')
            return get_json(0, msg, {})
        if User.query.filter_by(username=username).exists():
            msg = _('The username has been registered')
            return get_json(0, msg, {})
        if password != confirm_password:
            msg = _('Two passwords are different')
            return get_json(0, msg, {})
        if not check_captcha(phone, captcha):
            msg = _('The captcha is error')
            return get_json(0, msg, {})
        user_code = self.user_code()
        user = User(username=username, phone=phone, user_code=user_code,
                    recommender_code=recommender_code, integral=100)
        recommender_user = User.query.filter_by(user_code=recommender_code).first()
        user.integral = user.integral+1
        if recommender_user:
            recommender_user.integral = user.integral+1
            recommender_user.save()
        user.set_password(password)
        user.save()
        redis_data.delete(phone)
        user.login(True)
        msg = _('You have registered')
        data = {"username":user.username}
        Avatar(data, user)
        return get_json(1, msg, data)

    def user_code(self):
        user_code = randint(10000, 99999)
        if User.query.filter_by(user_code=user_code).exists():
            return self.user_code()
        return user_code


class ForgetView(MethodView):
    decorators = [guest_required]

    def get(self):
        msg = _('forget password')
        return get_json(1, msg, {})

    def post(self):
        post_data = request.json
        email = post_data['email']
        user = User.query.filter_by(email = email, is_confirmed=1).first()
        if not user:
            msg = _('Email hasn\'t been binded, please find it through other ways.')
            return get_json(0, msg, {})
        self.send_email(user)
        msg = _('An email has been sent to you.Please receive and update your password in time')
        return get_json(1, msg, {})

    def send_email(self, user):
        token = user.email_token
        confirm_url = url_for(
            'auth.forget_token', token=token, _external=True)
        html = render_template('templet/forget.html', confirm_url=confirm_url)
        subject = _('Please set a new password')
        user.send_email(html=html, subject=subject)

class ForgetTokenView(MethodView):
    def get(self, token):
        user = User.check_email_token(token)
        if not user:
            msg = _('The confirm link has been out of time.Please confirm your email again')
            flash(msg)
            return redirect('/')
        return redirect('/#/findPwd/%s'%token)

class SetPasswordView(MethodView):
    def get(self):
        msg = _('Change Password')
        return get_json(1, msg, {})
    
    def post(self, token=None):
        post_data = request.json
        password = post_data['password']
        confirm_password = post_data['confirm_password']
        if 'phone' in post_data:
            phone = post_data['phone']
            user = User.query.filter_by(phone = phone).first()
        else:
            user = User.check_email_token(token)
        if password != confirm_password:
            msg = _('Two passwords are different')
            return get_json(0, msg, {})
        user.set_password(password)
        user.save()
        data = {"username":user.username}
        Avatar(data, user)
        msg = _('success')
        return get_json(1, msg, data)

class PhoneForgetView(MethodView):
    decorators = [guest_required]

    def get(self):
        msg = _('forget password')
        return get_json(1, msg, {})

    def post(self):
        post_data = request.json
        phone = post_data['phone']
        captcha = post_data['captcha']
        if not check_phone(phone):
            msg = _('The phone is error')
            return get_json(0, msg, {})
        if not check_captcha(phone, captcha):
            msg = _('The captcha is error')
            return get_json(0, msg, {})
        redis_data.delete(phone)
        msg = _('success')
        return get_json(1, msg, {})


class ConfirmView(MethodView):
    decorators = [login_required]
    
    def get(self):
        email = request.data.get('email')
        if User.query.filter_by(email=email, is_confirmed=1).exists():
            msg = _('The email has been registered')
            return get_json(0, msg, {})
        msg = _('success')
        return get_json(1, msg, {})

    def post(self):
        user = request.user
        email = request.data.get('email')
        if User.query.filter_by(email=email,is_confirmed=1).exists():
            msg = _('The email has been registered')
            return get_json(0, msg, {})
        self.send_email(user, email)
        msg = _('An email has been sent to you.Please receive and update your password in time')
        return get_json(1, msg, {})

    def send_email(self, user, email):
        token = user.email_token
        confirm_url = url_for(
            'auth.confirm_token', token=token, _external=True)
        html = render_template('templet/email.html', confirm_url=confirm_url)
        subject = _('Please confirm  your email')
        user.email = email
        user.save()
        user.send_email(html=html, subject=subject)
        

class ConfirmTokenView(MethodView):
    def get(self, token):
        user = User.check_email_token(token)
        if not user:
            msg = _('The confirm link has been out of time.Please confirm your email again')
            flash(msg)
            return redirect('/')
        user.is_confirmed = 1
        user.save()
        return redirect('/')

class ConfirmPhoneView(MethodView):
    def post(self):
        phone = request.json['phone']
        if (request.path.endswith('login') and check_phone(phone)) or (request.path.endswith('phoneCaptcha') and not check_phone(phone)):
            captcha = ''.join(sample(digits, 6))
            url = "http://www.kanyanbao.com/websocket/aip/send_sms.json"
            data = {"phone":phone, "content":_('Your verification code is %s, valid for 5 minutes.')%captcha}
            headers = {'Content-Type':'application/json'}
            ori = requests.post(url, headers = headers, json = data)
            redis_data.set(phone, captcha, ex=300)
            msg = _('The message has been sent')
            return get_json(1, msg, {})
        msg = _('failed')
        return get_json(0, msg, {})


class Auth(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        login_view = LoginView.as_view('auth.login')
        logout_view = LogoutView.as_view('auth.logout')
        register_view = RegisterView.as_view('auth.register')
        forget_view = ForgetView.as_view('auth.forget')
        #confirm_view = ConfirmView.as_view('auth.confirm')
        confirm_token_view = ConfirmTokenView.as_view('auth.confirm_token')
        forget_token_view = ForgetTokenView.as_view('auth.forget_token')
        phone_view = ConfirmPhoneView.as_view('phone')
        loginphone_view = ConfirmPhoneView.as_view('loginphone')
        phonelogin_view = PhoneLoginView.as_view('phonelogin')
        phoneforget_view = PhoneForgetView.as_view('phoneforget')
        emailsetpassword_view = SetPasswordView.as_view('mailsetpassword')
        phonesetpassword_view = SetPasswordView.as_view('phonesetpassword')
        settingemail_view = ConfirmView.as_view('setting.email')


        app.add_url_rule('/api/login', view_func=login_view)
        app.add_url_rule('/api/logout', view_func=logout_view)
        app.add_url_rule('/api/register', view_func=register_view)
        app.add_url_rule('/api/forget', view_func=forget_view)
        #app.add_url_rule('/api/confirm', view_func=confirm_view)
        app.add_url_rule('/api/confirm/<token>', view_func=confirm_token_view)
        app.add_url_rule('/api/forget/<token>', view_func=forget_token_view)
        app.add_url_rule('/api/phoneCaptcha', view_func=phone_view)
        app.add_url_rule('/api/phoneCaptcha/login', view_func=loginphone_view)
        app.add_url_rule('/api/phoneLogin', view_func=phonelogin_view)
        app.add_url_rule('/api/phoneForget', view_func=phoneforget_view)
        app.add_url_rule('/api/setpassword/<token>', view_func=emailsetpassword_view)
        app.add_url_rule('/api/setpassword', view_func=phonesetpassword_view)
        app.add_url_rule('/api/setting/email', view_func=settingemail_view)
