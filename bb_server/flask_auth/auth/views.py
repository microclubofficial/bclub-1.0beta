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
from flask_auth.babel import domain
from flask_auth.babel import gettext as _
from flask_auth.models import db
from forums.extension import redis_data
import requests

User = db.Model._decl_class_registry['User']


def guest_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        if current_user.is_authenticated:
            #flash(_("You have logined in ,needn't login again"))
            msg = _("You have logined in ,needn't login again")
            #return redirect('/')
            return get_json(1, msg, {})
        return func(*args, **kwargs)
    return decorator


def check_params(keys):
    def _check_params(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            post_data = request.json
            for key in keys:
                if not post_data.get(key):
                    msg = _('The %s is required'%key)
                    return get_json(0, msg, {}) 
            return func(*args, **kwargs)

        return decorator

    return _check_params

def check_phone(phone, captcha):
    redis_captcha = redis_data.get(phone)
    if not redis_captcha:
        return False
    if redis_captcha != captcha:
        return False
    return True

class LoginView(MethodView):
    decorators = [guest_required]

    def get(self):
        domain.as_default()
        #return render_template('auth/login.html')
        return get_json(1, '登录', {})

    @check_params(['username', 'password'])
    def post(self):
        post_data = request.json
        username = post_data['username']
        password = post_data['password']
        remember = post_data.pop('remember', True)
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            #msg = _('用户名或密码错误')
            #return HTTPResponse(HTTPResponse.HTTP_PARA_ERROR, message=msg).to_response()
            return get_json(0, '用户名或密码错误', {})
        captcha = post_data['captcha']
        session_captcha = session.pop('captcha', '00000')
        if captcha.lower() != session_captcha.lower():
            msg = _('The captcha is error')
            return get_json(0, msg, {})  
        user.login(remember)
        data = {"username":user.username}
        Avatar(data, user)
        #serializer = user.serializer if hasattr(
        #    user, 'serializer') else Serializer(user, depth=1)
        #return HTTPResponse(HTTPResponse.NORMAL_STATUS, data=serializer.data).to_response()
        return get_json(1, '登录成功', data)

class PhoneLoginView(MethodView):
    decorators = [guest_required]

    def get(self):
        domain.as_default()
        return get_json(1, '登录', {})

    @check_params(['phone', 'phonecaptcha'])
    def post(self):
        post_data = request.json
        phone = post_data['phone']
        captcha = post_data['phonecaptcha']
        remember = post_data.pop('remember', True)
        user = User.query.filter_by(phone=phone).first()
        if not user:
            return get_json(0, '手机号未注册', {})
        if not check_phone(phone, captcha):
            return get_json(0, '验证码错误', {})
        user.login(remember)
        data = {"username":user.username}
        Avatar(data, user)
        return get_json(1, '登录成功', data)
        

class LogoutView(MethodView):
    decorators = [login_required]

    def get(self):
        current_user.logout()
        #return redirect(request.args.get('next') or '/')
        return get_json(1, '登出成功', {})


class RegisterView(MethodView):
    def get(self):
        domain.as_default()
        #return render_template('auth/register.html')
        return get_json(1, '注册', {})

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
        if User.query.filter_by(phone=phone).exists():
            msg = _('The phone has been registered')
            #return HTTPResponse(HTTPResponse.HTTP_PARA_ERROR, message=msg).to_response()
            return get_json(0, msg, {})
        if User.query.filter_by(username=username).exists():
            msg = _('The username has been registered')
            #return HTTPResponse(HTTPResponse.HTTP_PARA_ERROR, message=msg).to_response()
            return get_json(0, msg, {})
        if password != confirm_password:
            msg = _('Two passwords are different')
            return get_json(0, msg, {})
        if not check_phone(phone, captcha):
            return get_json(0, '验证码错误', {})
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
        user.login(True)
        #self.send_email(user)
        #flash(_('An email has been sent to your.Please receive'))
        #msg = _('An email has been sent to your.Please receive')
        msg = _('注册成功')
        data = {"username":user.username}
        Avatar(data, user)
        #serializer = user.serializer if hasattr(
        #    user, 'serializer') else Serializer(user, depth=1)
        #return HTTPResponse(HTTPResponse.NORMAL_STATUS, data=serializer.data).to_response()
        return get_json(1, msg, data)

    def user_code(self):
        user_code = randint(10000, 99999)
        if User.query.filter_by(user_code=user_code).exists():
            return self.user_code()
        return user_code

    #def send_email(self, user):
    #    token = user.email_token
    #    confirm_url = url_for(
    #        'auth.confirm_token', token=token, _external=True)
    #    html = render_template('templet/email.html', confirm_url=confirm_url)
        #html = 'hello'
    #    subject = _("Please confirm  your email")
    #    user.send_email(html=html, subject=subject)


class ForgetView(MethodView):
    decorators = [guest_required]

    def get(self):
        print()
        domain.as_default()
        #return render_template('auth/forget.html')
        return get_json(1, '忘记密码', {})

    def post(self):
        post_data = request.json
        email = post_data['email']
        user = User.query.filter_by(email=email).first()
        if not user:
            msg = 'The email is error'
            #return HTTPResponse(HTTPResponse.HTTP_PARA_ERROR, message=msg).to_response()
            return get_json(0, msg, {})
        #password = ''.join(sample(ascii_letters + digits, 8))
        #user.set_password(password)
        #user.save()
        self.send_email(user)
        #flash(
        #   _('An email has been sent to you.'
        #    'Please receive and update your password in time'))
        msg = _('An email has been sent to you.Please receive and update your password in time')
        #return HTTPResponse(HTTPResponse.NORMAL_STATUS).to_response()
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
            msg = _('The confirm link has been out of time.'
                    'Please confirm your email again')
            flash(msg)
            return redirect('/')
        flash('You have confirmed your account. Thanks!')
        return redirect('/#/findPwd/%s'%token)

class SetPasswordView(MethodView):
    def get(self):
        domain.as_default()
        return get_json(1, '修改密码', {})
    
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
        user.login(True)
        data = {"username":user.username}
        Avatar(data, user)
        return get_json(1, '修改成功', data)

class PhoneForgetView(MethodView):
    decorators = [guest_required]

    def get(self):
        print()
        domain.as_default()
        return get_json(1, '忘记密码', {})

    def post(self):
        post_data = request.json
        phone = post_data['phone']
        captcha = post_data['captcha']
        user = User.query.filter_by(phone=phone).first()
        if not user:
            msg = 'The phone is error'
            return get_json(0, msg, {})
        if not check_phone(phone, captcha):
            return get_json(0, '验证码错误', {})
        return get_json(1, '验证成功', {})


class ConfirmView(MethodView):
    decorators = [login_required]

    def post(self):
        if request.path.endswith('mail'):
            user = request.user
            email = request.values.get('email')
            user.email = email
            user.save()
        elif current_user.is_confirmed:
            #return HTTPResponse(HTTPResponse.USER_IS_CONFIRMED).to_response()
            return get_json(1, '用户已通过确认', {})
        self.send_email(current_user)
        #return HTTPResponse(HTTPResponse.NORMAL_STATUS,
        # description=_('An email has been sent to your.Please receive')).to_response()
        return get_json(1, '一封邮件已发出', {})

    def send_email(self, user):
        token = user.email_token
        confirm_url = url_for(
            'auth.confirm_token', token=token, _external=True)
        html = render_template('templet/email.html', confirm_url=confirm_url)
        subject = _("Please confirm  your email")
        user.send_email(html=html, subject=subject)

class ConfirmTokenView(MethodView):
    def get(self, token):
        user = User.check_email_token(token)
        if not user:
            msg = _('The confirm link has been out of time.'
                    'Please confirm your email again')
            flash(msg)
            return redirect('/')
        if user.is_confirmed:
            flash(_('The email has been confirmed. Please login.'))
            return redirect('/')
        user.is_confirmed = True
        user.save()
        flash('You have confirmed your account. Thanks!')
        return redirect('/')

class ConfirmPhoneView(MethodView):
    def post(self):
        phone = request.json['phone']
        captcha = ''.join(sample(digits, 6))
        url = "http://www.kanyanbao.com/websocket/aip/send_sms_template.json"
        data = {"phone":phone, "templateId": "1001", "content":captcha}
        headers = {'Content-Type':'application/json'}
        ori = requests.post(url, headers = headers, json = data)
        redis_data.set(phone, captcha, ex=300)
        return get_json(1, '短信发送成功', {})

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
        confirm_view = ConfirmView.as_view('auth.confirm')
        confirm_token_view = ConfirmTokenView.as_view('auth.confirm_token')
        forget_token_view = ForgetTokenView.as_view('auth.forget_token')
        phone_view = ConfirmPhoneView.as_view('phone')
        phonelogin_view = PhoneLoginView.as_view('phonelogin')
        phoneforget_view = PhoneForgetView.as_view('phoneforget')
        emailsetpassword_view = SetPasswordView.as_view('mailsetpassword')
        phonesetpassword_view = SetPasswordView.as_view('phonesetpassword')
        settingemail_view = ConfirmView.as_view('setting.email')

        app.add_url_rule('/api/login', view_func=login_view)
        app.add_url_rule('/api/logout', view_func=logout_view)
        app.add_url_rule('/api/register', view_func=register_view)
        app.add_url_rule('/api/forget', view_func=forget_view)
        app.add_url_rule('/api/confirm', view_func=confirm_view)
        app.add_url_rule('/api/confirm/<token>', view_func=confirm_token_view)
        app.add_url_rule('/api/forget/<token>', view_func=forget_token_view)
        app.add_url_rule('/api/phoneCaptcha', view_func=phone_view)
        app.add_url_rule('/api/phoneLogin', view_func=phonelogin_view)
        app.add_url_rule('/api/phoneForget', view_func=phoneforget_view)
        app.add_url_rule('/api/setpassword/<token>', view_func=emailsetpassword_view)
        app.add_url_rule('/api/setpassword', view_func=phonesetpassword_view)
        app.add_url_rule('/api/setting/email', view_func=settingemail_view)
