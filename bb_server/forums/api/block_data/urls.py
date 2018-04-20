from flask import Blueprint
from .views import Currency_News, B_List, Picture, K_Line, SideBar

site = Blueprint('blockcc', __name__, url_prefix='/api')

currency_news = Currency_News.as_view('currency_news')
b_list = B_List.as_view('b_list')
k_line = K_Line.as_view('k_line')
b_picture = Picture.as_view('b_picture')
sidebar = SideBar.as_view('sidebar')

site.add_url_rule('/currency_news/<token>', view_func=currency_news)
site.add_url_rule('/blist/<page>/<limit>', view_func=b_list)
site.add_url_rule('/bpicture', view_func=b_picture)
site.add_url_rule('/kline/<token>', view_func=k_line)
site.add_url_rule('/side/tokenintroduce/<token>', view_func=sidebar)

def init_app(app):
    app.register_blueprint(site)