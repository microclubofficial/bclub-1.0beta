from flask import Blueprint
from .views import BarListView, BarView, BarAnswerView, BarCommentreplyView, BarQuestionView, BarQuestionreplyView

site = Blueprint('bar', __name__, url_prefix='/api/bar')

barlist_view = BarListView.as_view('barlist')
bar_view = BarView.as_view('bar')
barquestion_view = BarQuestionView.as_view('bar_question')
baranswer_comment_view = BarAnswerView.as_view('bar_answer')
barquestion_reply_view = BarQuestionreplyView.as_view('bar_question_reply')
barcomment_reply_view = BarCommentreplyView.as_view('bar_reply')

site.add_url_rule('', view_func=barlist_view)
site.add_url_rule('/<int:id>', view_func=bar_view)
site.add_url_rule('/question/<int:id>', view_func=barquestion_view)
site.add_url_rule('/answer/replies/<int:id>', view_func=baranswer_comment_view)
site.add_url_rule('/question/replies/<int:id>', view_func=barquestion_reply_view)
site.add_url_rule('/comment/replies/<int:id>', view_func=barcomment_reply_view)

def init_app(app):
    app.register_blueprint(site)