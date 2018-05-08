from flask import current_app, request
from flask.views import MethodView
from forums.func import get_json
from forums.api.user.models import User
from forums.func import get_json, object_as_dict, time_diff, Avatar, FindAndCount, Count
from .models import Bar, Questions, Answers, Comments#, Replys
from .permissions import reply_list_permission
import json
import math

per_page = 5

class BarListView(MethodView):
    def get(self, page):
        start = (page-1)*per_page
        barlists = Bar.query.limit(per_page).offset(start)
        bar_count = FindAndCount(Bar)
        page_count = int(math.ceil(bar_count/per_page))
        bar_questions = Questions.query.filter_by(bar_id = 1, is_bar=1).first()
        user = bar_questions.author
        #user = User.query.filter_by(id = bar_questions.author_id).first()
        bar = Bar.query.filter_by(id = bar_questions.bar_id).first()
        question = object_as_dict(bar_questions)
        Avatar(question, user)
        question['author'] = user.username
        question['bar'] = bar.title
        barlist = []
        for i in barlists:
            user = i.author
            picture = i.picture
            bar_data = object_as_dict(i)
            bar_data['content'] = json.loads(bar_data['content'])
            bar_data['author'] = user.username  
            bar_data['picture'] = picture
            barlist.append(bar_data)
        data = {'barlist': barlist, 'barquestion': question, 'page_count':page_count}
        return get_json(1, 'bar列表', data)

class BarView(MethodView):
    def get(self, id, page):
        start = (page-1)*per_page
        bar_questions = Questions.query.filter_by(bar_id = id, is_bar=1).limit(per_page).offset(start)
        question_count = FindAndCount(Questions)
        page_count = int(math.ceil(question_count/per_page))
        question_list = []
        for i in bar_questions:
            user = i.author
            answers_count = FindAndCount(Answers, questions_id = i.id, is_reply = 0)
            #try:
            #    bar_reply = Answers.query.filter_by(bar_topic_id = i.id).count()
            #except:
            #    bar_reply = 0
            diff_time = time_diff(i.updated_at)
            i.created_at = str(i.created_at)
            i.updated_at = str(i.updated_at)
            questions_data = object_as_dict(i)
            questions_data['content'] = json.loads(questions_data['content'])
            questions_data['author'] = user.username
            questions_data['diff_time'] = diff_time
            questions_data['answers_count'] = answers_count
            questions_data['is_good'], questions_data['is_good_bool'] = Count(i.is_good)
            questions_data['is_bad'], questions_data['is_bad_bool'] = Count(i.is_bad)
            Avatar(questions_data, user)
            question_list.append(questions_data)
        data = {'question_list':question_list, 'page_count':page_count}
        return get_json(1, 'bar问题列表', data)

class BarQuestionView(MethodView):
    decorators = (reply_list_permission, )

    def get(self, id, page):
        start = (page-1)*per_page
        bar_question = Questions.query.filter_by(id = id).first()
        bar_answers = Answers.query.filter_by(questions_id = id, is_reply = 0).order_by('-id').limit(per_page).offset(start)
        answer_count = FindAndCount(Answers, is_reply = 0)
        page_count = int(math.ceil(answer_count/per_page))
        question_user = bar_question.author
        #question_user = User.query.filter_by(id = bar_question.author_id).first()
        diff_time = time_diff(bar_question.updated_at)
        bar_question.created_at = str(bar_question.created_at)
        bar_question.updated_at = str(bar_question.updated_at)
        questions_data = object_as_dict(bar_question)
        questions_data['content'] = json.loads(questions_data['content'])
        questions_data['diff_time'] = diff_time
        questions_data['author'] = question_user.username
        Avatar(questions_data, question_user)
        answers_list = []
        for i in bar_answers:
            answer_user = i.author
            diff_time = time_diff(i.updated_at)
            i.created_at = str(i.created_at)
            i.updated_at = str(i.updated_at)
            answers_data = object_as_dict(i)
            answers_data['content'] = json.loads(answers_data['content'])
            answers_data['author'] = answer_user.username
            answers_data['diff_time'] = diff_time
            answers_data['is_good'], answers_data['is_good_bool'] = Count(i.is_good)
            answers_data['is_bad'], answers_data['is_bad_bool'] = Count(i.is_bad)
            Avatar(answers_data, answer_user)
            answers_list.append(answers_data)
        data = {'question':questions_data, 'answers':answers_list, 'page_count':page_count}
        return get_json(1, 'bar问题详情页', data)

    def post(self, id):
        qusetion = Questions.query.filter_by(id = id).first_or_404()
        post_data = request.data
        user = request.user
        content = post_data.pop('content', None)
        bar_answer = Answers(content = json.dumps(content), questions_id = id, is_reply = 0)
        bar_answer.author_id = user.id
        bar_answer.save()
        bar_answer.created_at = str(bar_answer.created_at)
        bar_answer.updated_at = str(bar_answer.updated_at)
        answers_data = object_as_dict(bar_answer)
        answers_data['content'] = json.loads(answers_data['content'])
        answers_data['author'] = user.username
        answers_data['diff_time'] = '0秒'
        answers_data['is_good'] = 0
        answers_data['is_bad'] = 0
        Avatar(answers_data, user)
        return get_json(1, '回答成功', answers_data)

class BarAnswerView(MethodView):
    decorators = (reply_list_permission, )

    def get(self, id, page):
        start = (page-1)*per_page
        comment = Comments.query.filter_by(answers_id = id).order_by('-id').limit(per_page).offset(start)
        comment_count = FindAndCount(Comments)
        page_count = int(math.ceil(comment_count/per_page))
        comments_list = []
        for i in comment:
            comment_user = i.author
            #comment_user = User.query.filter_by(id = i.author_id).first()
            diff_time = time_diff(i.updated_at)
            i.created_at = str(i.created_at)
            i.updated_at = str(i.updated_at)
            comments_data = object_as_dict(i)
            comments_data['content'] = json.loads(comments_data['content'])
            comments_data['diff_time'] = diff_time
            comments_data['author'] = comment_user.username
            comments_data['is_good'], comments_data['is_good_bool'] = Count(i.is_good)
            comments_data['is_bad'], comments_data['is_bad_bool'] = Count(i.is_bad)
            Avatar(comments_data, comment_user)
            comments_list.append(comments_data)
        data = {'comments_list':comments_list, 'page_count':page_count} 
        return get_json(1, '回答的评论列表', data)
    
    def post(self, id):
        post_data = request.data
        user = request.user
        content = post_data.pop('content', None)
        reference = post_data.pop('replyContent', None)
        at_user = post_data.pop('author', None)
        answer_comment = Comments(content = json.dumps(content), answers_id = id, reference = reference, at_user = at_user)
        answer_comment.author_id = user.id
        answer_comment.save()
        answer_comment.created_at = str(answer_comment.created_at)
        answer_comment.updated_at = str(answer_comment.updated_at)
        comments_data = object_as_dict(answer_comment)
        comments_data['content'] = json.loads(comments_data['content'])
        comments_data['author'] = user.username
        comments_data['diff_time'] = '0秒'
        comments_data['is_good'] = 0
        comments_data['is_bad'] = 0
        Avatar(comments_data, user)
        return get_json(1, '评论成功', comments_data)

class BarQuestionreplyView(MethodView):
    decorators = (reply_list_permission, )

    def get(self, id, page):
        start = (page-1)*per_page
        bar_replies = Answers.query.filter_by(questions_id = id, is_reply = 1).order_by('-id').limit(per_page).offset(start)
        reply_count = FindAndCount(Answers, is_reply = 1)
        page_count = int(math.ceil(reply_count/per_page))
        replies = []
        for i in bar_replies: 
            user = i.author
            #user = User.query.filter_by(id = i.author_id).first()
            diff_time = time_diff(i.updated_at)
            i.created_at = str(i.created_at)
            i.updated_at = str(i.updated_at)
            replies_data = object_as_dict(i)
            replies_data['content'] = json.loads(replies_data['content'])
            replies_data['author'] = user.username
            replies_data['diff_time'] = diff_time
            replies_data['is_good'], replies_data['is_good_bool'] = Count(i.is_good)
            replies_data['is_bad'], replies_data['is_bad_bool'] = Count(i.is_bad)
            Avatar(replies_data, user)
            replies.append(replies_data)
        data = {'replies':replies, 'page_count':page_count}
        return get_json(1, '评论信息', data)

    def post(self, id):
        post_data = request.data
        user = request.user
        content = post_data.pop('content', None)
        bar_reply = Answers(content = json.dumps(content), questions_id = id, is_reply = 1)
        bar_reply.author_id = user.id
        bar_reply.save()
        diff_time = time_diff(bar_reply.updated_at)
        bar_reply.created_at = str(bar_reply.created_at)
        bar_reply.updated_at = str(bar_reply.updated_at)
        replies_data = object_as_dict(bar_reply)
        replies_data['content'] = json.loads(replies_data['content'])
        replies_data['author'] = user.username
        replies_data['diff_time'] = diff_time
        replies_data['is_good'] = 0
        replies_data['is_bad'] = 0
        Avatar(replies_data, user)
        return get_json(1, '评论成功', replies_data)

'''class BarCommentreplyView(MethodView):
    decorators = (reply_list_permission, )

    def post(self, id):
        comment = Comments.query.filter_by(id=id).first_or_404()
        post_data = request.data
        user = request.user
        content = post_data.pop('content', None)
        comment_reply = Replys(content = content, comments_id = id)
        comment_reply.author_id = user.id
        comment_reply.save()
        diff_time = time_diff(comment_reply.updated_at)
        comment_reply.created_at = str(comment_reply.created_at)
        comment_reply.updated_at = str(comment_reply.updated_at)
        replies_data = object_as_dict(comment_reply)
        replies_data['author'] = user.username
        replies_data['diff_time'] = diff_time
        Avatar(replies_data, user)
        comments = dict()
        comments['comment_author'] = User.query.filter_by(id = comment.author_id).first().username
        comments['content'] = comment.content
        data = {'comment':comments, 'replies':replies_data}
        return get_json(1, '回复成功', data)'''
