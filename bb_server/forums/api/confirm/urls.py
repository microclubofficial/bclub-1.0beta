from flask import Blueprint
from .views import PasswordView, EmailView

site = Blueprint('confirm', __name__, url_prefix='/api/confirmed')
password_view = PasswordView.as_view('password')
email_view = EmailView.as_view('email')

site.add_url_rule('/password', view_func=password_view)
site.add_url_rule('/email', view_func=email_view)

def init_app(app):
    app.register_blueprint(site)
    