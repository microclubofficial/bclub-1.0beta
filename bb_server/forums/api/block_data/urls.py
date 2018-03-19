from flask import Blueprint
from .views import B_Price

site = Blueprint('api', __name__, url_prefix='/api/price')

price_view = B_Price.as_view('blockcc_data')

site.add_url_rule('/btc', view_func=price_view)

def init_app(app):
    app.register_blueprint(site)