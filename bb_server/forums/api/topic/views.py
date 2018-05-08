#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-15 22:07:39 (CST)
# Last Update: 星期日 2018-02-11 15:07:05 (CST)
#          By:
# Description:
# **************************************************************************
from flask import Markup, redirect, render_template, request, url_for, current_app
from flask_babelex import gettext as _
from flask_login import current_user, login_required

from flask_auth.form import form_validate
from flask_auth.response import HTTPResponse
from forums.api.forms import (CollectForm, ReplyForm, TopicForm,
                              collect_error_callback, error_callback,
                              form_board)
from forums.api.forums.models import Board
from forums.api.bar.models import Questions, Answers, Comments
from forums.api.tag.models import Tags
from forums.api.utils import gen_topic_filter, gen_topic_orderby
from forums.common.serializer import Serializer
from forums.common.utils import gen_filter_dict, gen_order_by
from flask.views import MethodView
from forums.common.views import IsAuthMethodView, IsConfirmedMethodView

from forums.jinja import safe_markdown

from .models import Reply, Topic
from .permissions import (like_permission, reply_list_permission,
                          reply_permission, topic_list_permission,
                          topic_permission, edit_permission, thumd_permission)
from forums.api.message.models import MessageClient
from forums.func import get_json, object_as_dict, time_diff, FindAndCount, Avatar, Count
from forums.api.user.models import User
from forums.api.collect.models import Collect
from sqlalchemy import func
import math
import json

per_page = 5

def collect_bool(topicid):
    if current_user.is_authenticated: 
        topic_id = Collect.query.with_entities(Collect.topic_id).filter_by(author_id = request.user.id).first()
        if not topic_id:
            return False
        if topicid in json.loads(topic_id[0]):
            return True
        else:
            return False
    return False

class TopicAskView(IsConfirmedMethodView):
    def get(self):
        boardId = request.args.get('boardId', type=int)
        form = form_board()
        if boardId is not None:
            form.category.data = boardId
        data = {'title': _('Ask - '), 'form': form}
        return render_template('topic/ask.html', **data)


class TopicEditView(IsConfirmedMethodView):
    decorators = (edit_permission, )

    def get(self, topicId):
        topic = Topic.query.filter_by(id=topicId).first_or_404()
        form = form_board()
        form.title.data = topic.title
        form.category.data = topic.board_id
        form.tags.data = ','.join([tag.name for tag in topic.tags])
        form.content.data = topic.content
        data = {'title': _('Edit -'), 'form': form, 'topic': topic}
        return render_template('topic/edit.html', **data)


class TopicPreviewView(IsConfirmedMethodView):
    @login_required
    def post(self):
        post_data = request.data
        content_type = post_data.pop('content_type', None)
        content = post_data.pop('content', None)
        if content_type == Topic.CONTENT_TYPE_MARKDOWN:
            return safe_markdown(content)
        return content


class TopicListView(MethodView):
    decorators = (topic_list_permission, )

    def get(self, page, token=None):
        start = (page-1)*per_page
        query_dict = request.data
        keys = ['title']
        #order_by = gen_topic_orderby(query_dict, keys)
        #filter_dict = gen_topic_filter(query_dict, keys)
        filter_dict = {}
        title = _('All Topics') 
        if 'token' in request.path:
            filter_dict.update(token=token)
            title = _(token+'Topics')
        #elif request.path.endswith('top'):
        #    filter_dict.update(is_bad=True)
        #    title = _('bad Topics')
        topics = Topic.query.filter_by(**filter_dict).order_by('-id').limit(per_page).offset(start)
        topic_count = FindAndCount(Topic)
        page_count = int(math.ceil(topic_count/per_page))
        topic = []
        for i in topics:
            user = i.author
            #user = User.query.filter_by(id = i.author_id).first()
            reply = Reply.query.filter_by(topic_id = i.id).order_by('-id').first()
            if reply:
                reply_user = reply.author.username
                #reply_id = reply.author_id
                #reply_user = User.query.filter_by(id = reply_id).first().username
                reply_time = time_diff(reply.updated_at)
            else:
                reply_user = None
                reply_time = None
            reply_count = FindAndCount(Reply, topic_id = i.id)
            diff_time = time_diff(i.updated_at)
            i.created_at = str(i.created_at)
            i.updated_at = str(i.updated_at)
            collect = collect_bool(i.id)
            topics_data = object_as_dict(i)
            topics_data['reply_time'] = reply_time
            topics_data['reply_user'] = reply_user
            topics_data['author'] = user.username
            topics_data['diff_time'] = diff_time
            topics_data['replies_count'] = reply_count
            topics_data['is_good'], topics_data['is_good_bool'] = Count(i.is_good)
            topics_data['is_bad'], topics_data['is_bad_bool'] = Count(i.is_bad)
            topics_data['collect_bool'] = collect
            Avatar(topics_data, user)
            topic.append(topics_data)
        data = {'classification': title, 'topics': topic, 'topic_count':topic_count, 'page_count':page_count}
        return get_json(1, '文章列表', data)

    #@form_validate(form_board, error=error_callback, f='')
    def post(self):
        user = request.user
        #form = TopicForm()
        #post_data = form.data
        post_data = request.data
        title = post_data.pop('title', None)
        content = post_data.pop('content', None)
        #tags = post_data.pop('tags', None)
        content_type = post_data.pop('content_type', 0)
        token = post_data.pop('token', None)
        picture = post_data.pop('picture', None)
        #board = post_data.pop('category', None)
        topic = Topic(
            title=title,
            content=content,
            content_type=content_type,
            token = token,
            picture = picture)
            #board_id=int(board))
        #tags = tags.split(',')
        #topic_tags = []
        #for tag in tags:
        #    tag = tag.strip()
        #    topic_tag = Tags.query.filter_by(name=tag).first()
        #    if topic_tag is None:
        #        topic_tag = Tags(name=tag, description=tag)
        #        topic_tag.save()
        #    topic_tags.append(topic_tag)
        #topic.tags = topic_tags
        #user = User.query.filter_by(id=1).first()
        topic.author = user
        topic.save()
        diff_time = time_diff(topic.updated_at)
        topic = object_as_dict(topic)
        Avatar(topic, user)
        topic['author'] = user.username
        topic['is_good'] = 0
        topic['is_bad'] = 0
        topic['diff_time'] = '0秒'
        #topic.board.topic_count = 1
        #topic.board.post_count = 1
        #topic.author.topic_count = 1
        #topic.reply_count = 1
        return get_json(1, '发表成功', topic)
        #return redirect(url_for('topic.topic', topicId=topic.id))

class TopicView(MethodView):
    decorators = (topic_permission, )
    
    def get(self, topicId, page):
        #form = ReplyForm()
        start = (page-1)*per_page
        query_dict = request.data
        topic = Topic.query.filter_by(id=topicId).first_or_404()
        diff_time = time_diff(topic.updated_at)
        topic.created_at = str(topic.created_at)
        topic.updated_at = str(topic.updated_at)
        #page, number = self.page_info
        #order_by = gen_order_by(query_dict, keys)
        #filter_dict = gen_filter_dict(query_dict, keys)
        reply = Reply.query.filter_by(topic_id = topicId).order_by(('-id')).limit(per_page).offset(start)
        reply_count = FindAndCount(Reply, topic_id = topicId)
        page_count = int(math.ceil(reply_count/per_page))
        replies = []
        for i in reply: 
            user = i.author
            #user = User.query.filter_by(id = i.author_id).first()
            diff_time = time_diff(i.updated_at)
            i.created_at = str(i.created_at)
            i.updated_at = str(i.updated_at)
            replies_data = object_as_dict(i)
            replies_data['author'] = user.username
            replies_data['diff_time'] = diff_time
            replies_data['is_good'], replies_data['is_good_bool'] = Count(i.is_good)
            replies_data['is_bad'], replies_data['is_bad_bool'] = Count(i.is_bad)
            Avatar(replies_data, user)
            replies.append(replies_data)
        topic_user = topic.author   
        topic_data = object_as_dict(topic)
        #topic_user = User.query.filter_by(id=topic_data['author_id']).first()
        topic_data['author'] = topic_user.username
        topic_data['diff_time'] = diff_time
        topic_data['is_good'], topic_data['is_good_bool'] = Count(topic.is_good)
        topic_data['is_bad'], topic_data['is_bad_bool'] = Count(topic.is_bad)
        topic_data['collect_bool'] = collect_bool(topicId)
        Avatar(topic_data, topic_user)
        data = {
            #'title': topic['title'],
            #'form': object_as_dict(form),
            'topic': topic_data,
            'replies': replies,
            'replies_count': reply_count,
            'page_count': page_count
        }
        #topic.read_count = 1
        return get_json(1,'文章详情',data)
        #return render_template('topic/topic.html', **data)

    @form_validate(form_board)
    def put(self, topicId):
        form = form_board()
        post_data = form.data
        topic = Topic.query.filter_by(id=topicId).first_or_404()
        title = post_data.pop('title', None)
        content = post_data.pop('content', None)
        content_type = post_data.pop('content_type', None)
        category = post_data.pop('category', None)
        if title is not None:
            topic.title = title
        if content is not None:
            topic.content = content
        if content_type is not None:
            topic.content_type = content_type
        if category is not None:
            topic.board_id = int(category)
        topic.save()
        return HTTPResponse(HTTPResponse.NORMAL_STATUS).to_response()


class ReplyListView(MethodView):
    def get(self, topicId, page):
        start = (page-1)*per_page
        reply = Reply.query.filter_by(topic_id = topicId).order_by(('-id')).limit(per_page).offset(start)
        reply_count = FindAndCount(Reply, topic_id = topicId)
        page_count = int(math.ceil(reply_count/per_page))
        data = []
        for i in reply: 
            user = i.author
            #user = User.query.filter_by(id = i.author_id).first()
            diff_time = time_diff(i.updated_at)
            i.created_at = str(i.created_at)
            i.updated_at = str(i.updated_at)
            replies_data = object_as_dict(i)
            replies_data['author'] = user.username
            replies_data['diff_time'] = diff_time
            replies_data['is_good'], replies_data['is_good_bool'] = Count(i.is_good)
            replies_data['is_bad'], replies_data['is_bad_bool'] = Count(i.is_bad)
            Avatar(replies_data, user)
            data.append(replies_data)
        data.append({'page_count':page_count, 'reply_count':reply_count}) 
        return get_json(1, '评论信息', data)

    decorators = (reply_list_permission, )
    #@form_validate(ReplyForm, error=error_callback, f='')
    def post(self, topicId):
        #topic = Topic.query.filter_by(id=topicId).first_or_404()
        post_data = request.data
        user = request.user
        content = post_data.pop('content', None)
        reference = post_data.pop('replyContent', None)
        at_user = post_data.pop('author', None)
        reply = Reply(content=content, reference = reference, topic_id = topicId, at_user = at_user)
        #user = User.query.filter_by(id=1).first()
        reply.author_id = user.id
        reply.save()
        reply.created_at = str(reply.created_at)
        reply.updated_at = str(reply.updated_at)
        replies_data = object_as_dict(reply)
        Avatar(replies_data, user)
        replies_data['author'] = user.username
        replies_data['is_good'] = 0
        replies_data['is_bad'] = 0
        replies_data['diff_time'] = '0秒'
        # noticetopicId
        #MessageClient.topic(reply)
        # count
        #topic.board.post_count = 1
        #reply.author.reply_count = 1
        return get_json(1, '评论成功', replies_data)
        #return redirect(url_for('topic.topic', topicId=topic.id))

'''   
class ReplyView(MethodView):
    
    decorators = (reply_permission, )
    def post(self, replyId):
        reply = Reply.query.filter_by(id=replyId).first_or_404()
        reply_data = dict()
        reply_data['author'] = User.query.filter_by(id = reply.author_id).first().username
        reply_data['content'] = reply.content
        post_data = request.data
        user = request.user
        content = post_data.pop('content', None)
        comment = Reply(content=content, topic_id = reply.id)
        comment.author_id = user.id
        comment.save()
        diff_time = time_diff(comment.updated_at)
        comment.created_at = str(comment.created_at)
        comment.updated_at = str(comment.updated_at)
        comment_data = object_as_dict(comment)
        Avatar(comment_data, user)
        comment_data['author'] = user.username
        comment_data['is_good'] = 0
        comment_data['is_bad'] = 0
        data = {'reply_data':reply_data, 'comment_data':comment_data}
        return get_json(1, '回复成功', data)


class ReplyView(MethodView):

    decorators = (reply_permission, )

    def put(self, replyId):
        post_data = request.data
        reply = Reply.query.filter_by(id=replyId).first_or_404()
        content = post_data.pop('content', None)
        if content is not None:
            reply.content = content
        reply.save()
        return HTTPResponse(HTTPResponse.NORMAL_STATUS).to_response()

    def delete(self, replyId):
        reply = Reply.query.filter_by(id=replyId).first_or_404()
        reply.delete()
        return HTTPResponse(HTTPResponse.NORMAL_STATUS).to_response()
'''

class LikeView(MethodView):

    decorators = (like_permission, )

    def post(self, replyId):
        user = request.user
        reply = Reply.query.filter_by(id=replyId).first_or_404()
        reply.likers.append(user)
        reply.save()
        MessageClient.like(reply)
        serializer = Serializer(reply, many=False)
        return HTTPResponse(
            HTTPResponse.NORMAL_STATUS, data=serializer.data).to_response()

    def delete(self, replyId):
        user = request.user
        reply = Reply.query.filter_by(id=replyId).first_or_404()
        reply.likers.remove(user)
        reply.save()
        serializer = Serializer(reply, many=False)
        return HTTPResponse(
            HTTPResponse.NORMAL_STATUS, data=serializer.data).to_response()

class ThumbView(IsAuthMethodView):
    #decorators = (thumd_permission, )

    def get(self, id, thumb):
        user = request.user
        if 'topic' in request.path:
            session = Topic.query.filter_by(id = id).first()
        elif 'reply' in request.path:
            session = Reply.query.filter_by(id = id).first()
        elif 'question' in request.path:
            session = Questions.query.filter_by(id = id).first()
        elif 'answer' in request.path:
            session = Answers.query.filter_by(id = id).first()
        elif 'comment' in request.path:
            session = Comments.query.filter_by(id = id).first() 
        userlist_good = json.loads(session.is_good)
        userlist_bad = json.loads(session.is_bad)
        if thumb == 'up':
            if user.id in userlist_good:
                return get_json(0, '不能重复点赞', len(userlist_good))
            elif user.id in userlist_bad:
                userlist_bad.remove(user.id)
            userlist_good.append(user.id)
            #good_count = len(userlist_good)
            #bad_count = len(userlist_bad)
            session.is_good = json.dumps(userlist_good)
            session.is_bad = json.dumps(userlist_bad)
        elif thumb == 'down':
            if user.id in userlist_bad:
                return get_json(0, '不能重复吐槽', len(userlist_bad))
            elif user.id in userlist_good:
                userlist_good.remove(user.id)
            userlist_bad.append(user.id)
            #good_count = len(userlist_good)
            #bad_count = len(userlist_bad)
            session.is_good = json.dumps(userlist_good)
            session.is_bad = json.dumps(userlist_bad)
        session.save()
        #data = {'good_count':good_count, 'bad_count':bad_count}
        data = {}
        data['is_good'], data['is_good_bool'] = Count(session.is_good)
        data['is_bad'], data['is_bad_bool'] = Count(session.is_bad)
        return get_json(1, '成功', data)
