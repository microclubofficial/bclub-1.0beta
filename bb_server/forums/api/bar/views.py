from flask import current_app, request
from flask.views import MethodView
from forums.func import get_json
from forums.api.user.models import User
from forums.func import get_json, object_as_dict, time_diff, Avatar
from .models import Bar, Questions, Answers, Comments, Replys
from .permissions import reply_list_permission


class BarListView(MethodView):
    def get(self):
        barlists = Bar.query.all()
        bar_questions = Questions.query.filter_by(bar_id = 1, is_bar=1).first()
        user = User.query.filter_by(id = bar_questions.author_id).first()
        bar = Bar.query.filter_by(id = bar_questions.bar_id).first()
        question = object_as_dict(bar_questions)
        Avatar(question, user)
        question['author'] = user.username
        question['bar'] = bar.title
        barlist = []
        for i in barlists:
            user = User.query.filter_by(id = i.author_id).first()
            picture = current_app.config['SERVER_URL'] + '/' + i.picture
            bar_data = object_as_dict(i)
            bar_data['author'] = user.username  
            bar_data['picture'] = picture
            barlist.append(bar_data)
        data = {'barlist': barlist, 'barquestion': question}
        return get_json(1, 'bar列表', data)

class BarView(MethodView):
    def get(self, id):
        bar_questions = Questions.query.filter_by(bar_id = id, is_bar=1).all()
        question_list = []
        for i in bar_questions:
            user = User.query.filter_by(id = i.author_id).first()
            try:
                bar_reply = Answers.query.filter_by(bar_topic_id = i.id).count()
            except:
                bar_reply = 0
            diff_time = time_diff(i.updated_at)
            i.created_at = str(i.created_at)
            i.updated_at = str(i.updated_at)
            questions_data = object_as_dict(i)
            questions_data['author'] = user.username
            questions_data['diff_time'] = diff_time
            questions_data['replies_count'] = bar_reply
            Avatar(questions_data, user)
            question_list.append(questions_data)
        return get_json(1, 'bar问题列表', question_list)

class BarQuestionView(MethodView):
    decorators = (reply_list_permission, )

    def get(self, id):
        bar_question = Questions.query.filter_by(id = id).first()
        bar_answers = Answers.query.filter_by(questions_id = id, is_reply = 0).order_by('-id').all()
        question_user = User.query.filter_by(id = bar_question.author_id).first()
        diff_time = time_diff(bar_question.updated_at)
        bar_question.created_at = str(bar_question.created_at)
        bar_question.updated_at = str(bar_question.updated_at)
        questions_data = object_as_dict(bar_question)
        questions_data['diff_time'] = diff_time
        questions_data['author'] = question_user.username
        Avatar(questions_data, question_user)
        answers_list = []
        for i in bar_answers:
            answer_user = User.query.filter_by(id = i.author_id).first()
            #comment = Comments.query.filter_by(answers_id = i.id, is_reply = 0).all()
            diff_time = time_diff(i.updated_at)
            i.created_at = str(i.created_at)
            i.updated_at = str(i.updated_at)
            answers_data = object_as_dict(i)
            answers_data['author'] = answer_user.username
            answers_data['diff_time'] = diff_time
            #comment_list = []
            #for j in comment:
            #    diff_time = time_diff(j.updated_at)
            #    comment_user = User.query.filter_by(id = j.author_id).first()
            #    j.created_at = str(j.created_at)
            #    j.updated_at = str(j.updated_at)
            #    comment_data = object_as_dict(j)
            #    comment_data['author'] = comment_user.username
            #    comment_data['diff_time'] = diff_time
            #    comment_list.append(comment_data)
            #answers_data['comments'] = comment_list
            Avatar(answers_data, answer_user)
            answers_list.append(answers_data)
        data = {'question':questions_data, 'answers':answers_list}
        return get_json(1, 'bar问题详情页', data)

    def post(self, id):
        qusetion = Questions.query.filter_by(id = id).first_or_404()
        post_data = request.data
        #user = request.user
        content = post_data.pop('content', None)
        bar_answer = Answers(content = content, questions_id = id, is_reply = 0)
        bar_answer.author_id = 6
        bar_answer.save()
        diff_time = time_diff(bar_answer.updated_at)
        answer_user = User.query.filter_by(id = bar_answer.author_id).first()
        bar_answer.created_at = str(bar_answer.created_at)
        bar_answer.updated_at = str(bar_answer.updated_at)
        answers_data = object_as_dict(bar_answer)
        answers_data['author'] = answer_user.username
        answers_data['diff_time'] = diff_time
        Avatar(answers_data, answer_user)
        return get_json(1, '回答成功', answers_data)

class BarAnswerView(MethodView):
    decorators = (reply_list_permission, )

    def get(self, id):
        comment = Comments.query.filter_by(answers_id = id).order_by('-id').all()
        comments_list = []
        for i in comment:
            comment_user = User.query.filter_by(id = i.author_id).first()
            replies = Replys.query.filter_by(comments_id = i.id).all()
            diff_time = time_diff(i.updated_at)
            i.created_at = str(i.created_at)
            i.updated_at = str(i.updated_at)
            comments_data = object_as_dict(i)
            comments_data['diff_time'] = diff_time
            comments_data['author'] = comment_user.username
            Avatar(comments_data, comment_user)
            comments_list.append(comments_data)
            replies_list = []
            for j in replies:
                diff_time = time_diff(j.updated_at)
                reply_user = User.query.filter_by(id = j.author_id).first()
                j.created_at = str(j.created_at)
                j.updated_at = str(j.updated_at)
                reply_data = object_as_dict(j)
                reply_data['author'] = reply_user.username
                reply_data['diff_time'] = diff_time
                replies_list.append(reply_data)
                Avatar(reply_data, reply_user)
            comments_data['replies'] = replies_list
        return get_json(1, '回答的评论列表', comments_list)
    
    def post(self, id):
        #Comment = Answers.query.filter_by(id = id).first_or_404()
        post_data = request.data
        #user = request.user
        content = post_data.pop('content', None)
        answer_comment = Comments(content = content, answers_id = id)
        answer_comment.author_id = 7
        answer_comment.save()
        diff_time = time_diff(answer_comment.updated_at)
        answer_user = User.query.filter_by(id = answer_comment.author_id).first()
        answer_comment.created_at = str(answer_comment.created_at)
        answer_comment.updated_at = str(answer_comment.updated_at)
        comments_data = object_as_dict(answer_comment)
        comments_data['author'] = answer_user.username
        comments_data['diff_time'] = diff_time
        Avatar(comments_data, answer_user)
        return get_json(1, '评论成功', comments_data)

class BarQuestionreplyView(MethodView):
    decorators = (reply_list_permission, )

    def get(self, id):
        bar_replies = Answers.query.filter_by(questions_id = id, is_reply = 1).order_by('-id').all()
        replies = []
        for i in bar_replies: 
            user = User.query.filter_by(id = i.author_id).first()
            diff_time = time_diff(i.updated_at)
            i.created_at = str(i.created_at)
            i.updated_at = str(i.updated_at)
            replies_data = object_as_dict(i)
            replies_data['author'] = user.username
            replies_data['diff_time'] = diff_time
            Avatar(replies_data, user)
            replies.append(replies_data)
        return get_json(1, '评论信息', replies)

    def post(self, id):
        qusetion = Questions.query.filter_by(id=id).first_or_404()
        post_data = request.data
        #user = request.user
        content = post_data.pop('content', None)
        bar_reply = Answers(content = content, questions_id = qusetion.id, is_reply = 1)
        bar_reply.author_id = 5
        bar_reply.save()
        diff_time = time_diff(bar_reply.updated_at)
        reply_user = User.query.filter_by(id = bar_reply.author_id).first()
        bar_reply.created_at = str(bar_reply.created_at)
        bar_reply.updated_at = str(bar_reply.updated_at)
        replies_data = object_as_dict(bar_reply)
        replies_data['author'] = reply_user.username
        replies_data['diff_time'] = diff_time
        Avatar(replies_data, reply_user)
        return get_json(1, '评论成功', object_as_dict(bar_reply))

class BarCommentreplyView(MethodView):
    decorators = (reply_list_permission, )

    def post(self, id):
        comment = Comments.query.filter_by(id=id).first_or_404()
        post_data = request.data
        #user = request.user
        content = post_data.pop('content', None)
        comment_reply = Replys(content = content, comments_id = id)
        comment_reply.author_id = 5
        comment_reply.save()
        diff_time = time_diff(comment_reply.updated_at)
        reply_user = User.query.filter_by(id = comment_reply.author_id).first()
        comment_reply.created_at = str(comment_reply.created_at)
        comment_reply.updated_at = str(comment_reply.updated_at)
        replies_data = object_as_dict(comment_reply)
        replies_data['author'] = reply_user.username
        replies_data['diff_time'] = diff_time
        Avatar(replies_data, reply_user)
        data = {'comment_content':comment.content,'replies':replies_data}
        return get_json(1, '评论成功', data)
