#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: models.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-03-28 17:58:59 (CST)
# Last Update:星期三 2017-12-13 16:06:36 (CST)
#          By:
# Description:
# **************************************************************************
from flask_auth.models import ModelMixin
from forums.api.user.models import User
from forums.extension import db


class Collect(db.Model, ModelMixin):
    __tablename__ = 'collects'
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.String(512), nullable='[]')
    author_id = db.Column(
        db.Integer, db.ForeignKey(
            'user.id', ondelete="CASCADE"))
    author = db.relationship(
        User,
        backref=db.backref(
            'collects', cascade='all,delete-orphan', lazy='dynamic', passive_deletes=True),
        lazy='joined')

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Collect %r>" % self.name
