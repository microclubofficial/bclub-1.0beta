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

from .views import (LikeView, ReplyListView, TopicAskView,ThumbView,
                    TopicEditView, TopicListView, TopicPreviewView, TopicView)

site = Blueprint('topic', __name__, url_prefix='/api' )

topic_list = TopicListView.as_view('list')
pull_topic = TopicListView.as_view('pull_list')
topic_good_list = TopicListView.as_view('good')
topic_token_list = TopicListView.as_view('topic_token_list')
topic = TopicView.as_view('topic')
ask_view = TopicAskView.as_view('ask')
edit_view = TopicEditView.as_view('edit')
preview_view = TopicPreviewView.as_view('preview')

reply_list = ReplyListView.as_view('reply_list')
reply_early = ReplyListView.as_view('reply_early')
reply_good = ReplyListView.as_view('reply_good')
put_reply = ReplyListView.as_view('put_reply')
#reply = ReplyView.as_view('reply')
like_view = LikeView.as_view('reply_like')
topic_thumb = ThumbView.as_view('topic_thumb')
reply_thumb = ThumbView.as_view('reply_thumb')

site.add_url_rule('/topic/ask', view_func=ask_view)
site.add_url_rule('/topic/preview', view_func=preview_view)
site.add_url_rule('/topic/<int:page>', view_func=topic_list)
site.add_url_rule('/topic', view_func=pull_topic)
site.add_url_rule('/topic/token/<token>/<int:page>', view_func=topic_token_list)
site.add_url_rule('/topic/good', view_func=topic_good_list)
site.add_url_rule('/topic/<int:topicId>/<int:page>', view_func=topic)
site.add_url_rule('/topic/edit/<int:topicId>', view_func=edit_view)
site.add_url_rule('/topic/replies/<int:topicId>/<int:page>', view_func=reply_list)
site.add_url_rule('/topic/replies/early/<int:topicId>/<int:page>', view_func=reply_early)
site.add_url_rule('/topic/replies/good/<int:topicId>/<int:page>', view_func=reply_good)
site.add_url_rule('/topic/replies/<int:topicId>', view_func=put_reply)
site.add_url_rule('/comment/replies/<int:topicId>', view_func=put_reply)
site.add_url_rule('/replies/<int:replyId>/like', view_func=like_view)
site.add_url_rule('/topic/<thumb>/<int:id>', view_func=topic_thumb)
site.add_url_rule('/reply/<thumb>/<int:id>', view_func=reply_thumb)

def init_app(app):
    app.register_blueprint(site)
