from flask import Blueprint
from .views import BarListView, BarView, BarAnswerView, BarQuestionView, BarQuestionreplyView

site = Blueprint('bar', __name__, url_prefix='/api/bar')

barlist_view = BarListView.as_view('barlist')
bar_view = BarView.as_view('bar_question_list')
barquestion_view = BarQuestionView.as_view('bar_question')
pull_barquestion_view = BarQuestionView.as_view('pull_bar_question')
baranswer_view = BarAnswerView.as_view('bar_answer')
pull_baranswer_view = BarAnswerView.as_view('pull_bar_answer')
barquestion_reply_view = BarQuestionreplyView.as_view('bar_question_reply')
pull_barquestion_reply_view = BarQuestionreplyView.as_view('pull_bar_question_reply')

site.add_url_rule('/<int:page>', view_func=barlist_view)
site.add_url_rule('/<int:id>/<int:page>', view_func=bar_view)
site.add_url_rule('/question/<int:id>/<int:page>', view_func=barquestion_view)
site.add_url_rule('/question/<int:id>', view_func=pull_barquestion_view)
site.add_url_rule('/answer/replies/<int:id>/<int:page>', view_func=baranswer_view)
site.add_url_rule('/answer/replies/<int:id>', view_func=pull_baranswer_view)
site.add_url_rule('/question/replies/<int:id>/<int:page>', view_func=barquestion_reply_view)
site.add_url_rule('/question/replies/<int:id>', view_func=pull_barquestion_reply_view)

def init_app(app):
    app.register_blueprint(site)