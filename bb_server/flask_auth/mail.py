#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# *************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: email.py
#   Author:JiangLin
#   Mail:xiyang0807@gmail.com
#   Created Time: 2015-11-27 21:59:02
# *************************************************************************
from flask_mail import Mail as _Mail
from flask_mail import Message
from threading import Thread
from itsdangerous import (URLSafeTimedSerializer, BadSignature,
                          SignatureExpired)
from flask import current_app
from .utils import gen_secret_key

mail = _Mail()


class Mail(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        mail.init_app(app)

    def send_async_email(self, msg):
        with self.app.app_context():
            mail.send(msg)

    def send_email(self, *args, **kwargs):
        msg = Message(*args, **kwargs)
        thr = Thread(target=self.send_async_email, args=[msg])
        thr.start()


class MailMixin(object):
    @property  
    def r_email(self):
        return self._r_email

    @r_email.setter    
    def r_email(self, email):
        self._r_email = email

    @property     
    def email_token(self):    
        config = current_app.config
        secret_key = config.setdefault('SECRET_KEY', gen_secret_key(24))
        salt = config.setdefault('SECRET_KEY_SALT', gen_secret_key(24))
        serializer = URLSafeTimedSerializer(secret_key, salt=salt)
        token = serializer.dumps([self.id, self._r_email])
        return token

    @classmethod
    def check_email_token(cls, token, max_age=86400):
        config = current_app.config
        secret_key = config.setdefault('SECRET_KEY', gen_secret_key(24))
        salt = config.setdefault('SECRET_KEY_SALT', gen_secret_key(24))
        serializer = URLSafeTimedSerializer(secret_key, salt=salt)
        try:
            id, email = serializer.loads(token, max_age=max_age)
        except SignatureExpired:
            return email, False
        except BadSignature:
            return email, False
        user = cls.query.filter_by(id=id).first()
        if user is None:
            return email, False
        return email, user

    # def send_email(self, *args, **kwargs):
    #     kwargs.update(recipients=[self.email])
    #     mail.send_email(*args, **kwargs)
