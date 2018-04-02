from flask import Blueprint
from .views import B_Price, B_Histery

site = Blueprint('blockcc', __name__, url_prefix='/api/price')

price_view = B_Price.as_view('blockcc_data')
history_view = B_Histery.as_view('blockcc_history')

site.add_url_rule('/<token>', view_func=price_view)
site.add_url_rule('/history/<token>/<limit>', view_func=history_view)

def init_app(app):
    app.register_blueprint(site)