from flask import Blueprint
from .views import Currency_News

site = Blueprint('blockcc', __name__, url_prefix='/api')

currency_news = Currency_News.as_view('currency_news')

site.add_url_rule('/currency_news/<token>', view_func=currency_news)


def init_app(app):
    app.register_blueprint(site)