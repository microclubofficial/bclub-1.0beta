from flask import Blueprint
from .views import Currency_News, B_List

site = Blueprint('blockcc', __name__, url_prefix='/api')

currency_news = Currency_News.as_view('currency_news')
b_list = B_List.as_view('b_list')

site.add_url_rule('/currency_news/<token>', view_func=currency_news)
site.add_url_rule('/blist/<page>/<limit>', view_func=b_list)

def init_app(app):
    app.register_blueprint(site)