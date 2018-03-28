#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: urls.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-15 22:15:34 (CST)
# Last Update:星期五 2017-11-10 10:57:47 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Blueprint

from .views import (LikeView, ReplyListView, ReplyView, TopicAskView,ThumbView,
                    TopicEditView, TopicListView, TopicPreviewView, TopicView)

site = Blueprint('topic', __name__, url_prefix='/api' )

topic_list = TopicListView.as_view('list')
pull_topic = TopicListView.as_view('pull_list')
topic_good_list = TopicListView.as_view('good')
topic_top_list = TopicListView.as_view('top')
topic = TopicView.as_view('topic')
ask_view = TopicAskView.as_view('ask')
edit_view = TopicEditView.as_view('edit')
preview_view = TopicPreviewView.as_view('preview')

reply_list = ReplyListView.as_view('reply_list')
put_reply = ReplyListView.as_view('put_reply')
reply = ReplyView.as_view('reply')
like_view = LikeView.as_view('reply_like')
thumb = ThumbView.as_view('thumb')

site.add_url_rule('/topic/ask', view_func=ask_view)
site.add_url_rule('/topic/preview', view_func=preview_view)
site.add_url_rule('/topic/<int:page>', view_func=topic_list)
site.add_url_rule('/topic', view_func=pull_topic)
site.add_url_rule('/topic/top', view_func=topic_top_list)
site.add_url_rule('/topic/good', view_func=topic_good_list)
site.add_url_rule('/topic/<int:topicId>/<int:page>', view_func=topic)
site.add_url_rule('/topic/edit/<int:topicId>', view_func=edit_view)
site.add_url_rule('/topic/replies/<int:topicId>/<int:page>', view_func=reply_list)
site.add_url_rule('/topic/replies/<int:topicId>', view_func=put_reply)
site.add_url_rule('/replies/<int:replyId>', view_func=reply)
site.add_url_rule('/replies/<int:replyId>/like', view_func=like_view)
site.add_url_rule('/topic/<int:topicId>/<thumb>', view_func=thumb)

def init_app(app):
    app.register_blueprint(site)
