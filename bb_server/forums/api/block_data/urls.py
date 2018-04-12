from flask import Blueprint
from .views import Currency_News, B_List, Picture

site = Blueprint('blockcc', __name__, url_prefix='/api')

currency_news = Currency_News.as_view('currency_news')
b_list = B_List.as_view('b_list')
b_picture = Picture.as_view('b_picture')

site.add_url_rule('/currency_news/<token>', view_func=currency_news)
site.add_url_rule('/blist/<page>/<limit>', view_func=b_list)
site.add_url_rule('/bpicture', view_func=b_picture)

def init_app(app):
    app.register_blueprint(site)