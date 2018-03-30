#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: config.example
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 12:31:46 (CST)
# Last Update: 星期日 2018-02-11 15:43:26 (CST)
#          By: jianglin
# Description:
# **************************************************************************
from datetime import timedelta
from os import path, pardir

DEBUG = True
SECRET_KEY = 'sinitek'
SESSION_COOKIE_DOMAIN = 'ymhui999.com:1234'
SECURITY_PASSWORD_SALT = '123!@#'
SECRET_KEY_SALT = '123^&*'

# avatar upload directory
AVATAR_FOLDER = path.join(path.abspath(path.dirname(__file__)), 'static/avatars')
# avatar generate range
AVATAR_RANGE = [122, 512]
PICTURE_FOLDER = path.join('static/avatars')
FILES_FOLDER = path.join('static/upload_files')
ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg', 'gif', 'txt', 'pdf', 'doc', 'docx'])

# for development use localhost:5000
# for production use xxx.com
# SERVER_NAME = 'localhost:5000'

# remember me to save cookies
PERMANENT_SESSION_LIFETIME = timedelta(days=3)
REMEMBER_COOKIE_DURATION = timedelta(days=3)
ONLINE_LAST_MINUTES = 5

# You want show how many topics per page
PER_PAGE = 12

# Use cache
CACHE_TYPE = 'redis'
CACHE_DEFAULT_TIMEOUT = 60
CACHE_KEY_PREFIX = 'cache:'
CACHE_REDIS_HOST = '127.0.0.1'
CACHE_REDIS_PORT = '6379'
CACHE_REDIS_PASSWORD = '940530'
CACHE_REDIS_DB = 2

# Redis setting
REDIS = {'db': 0, 'password': '940530', 'decode_responses': True}

# some middleware
MIDDLEWARE = ['forums.common.middleware.GlobalMiddleware',
              'forums.common.middleware.OnlineMiddleware',]

# Mail such as qq
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = "609313700"
MAIL_PASSWORD = "zxy940530"
MAIL_DEFAULT_SENDER = '609313700@qq.com'
# MAIL_SUPPRESS_SEND = True

#SERVER_NAME = ' https://nxqwazndlk.localtunnel.me:8000'
SERVER_URL = 'http://sinitek.ymhui999.com:1234'
SUBDOMAIN = {'forums': False, 'docs': False}

# logging setting
LOGGING = {
    'info': 'logs/info.log',
    'error': 'logs/error.log',
    'send_mail': False,
    'toaddrs': [],
    'subject': 'Your Application Failed',
    'formatter': '''
            Message type:       %(levelname)s
            Location:           %(pathname)s:%(lineno)d
            Module:             %(module)s
            Function:           %(funcName)s
            Time:               %(asctime)s

            Message:

            %(message)s
            '''
}

# Sql
#SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:940530@localhost/exampledb'
# SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

MSEARCH_INDEX_NAME = 'whoosh_index'
MSEARCH_BACKEND = 'whoosh'
SQLALCHEMY_ECHO = True
#SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://maple:Maple_sinitek1@192.168.3.194/maple_db'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:940530@127.0.0.1/maple_db?charset=utf8'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Locale
LANGUAGES = {'en': 'English', 'zh': 'Chinese'}
SITE = {'title': 'Honmaple', 'description': '爱生活，更爱自由', 'avatar': ''}
