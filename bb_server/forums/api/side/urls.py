from flask import Blueprint
from .views import (SideInfluence, SideAnalyst)

site = Blueprint('side', __name__, url_prefix='/api/side')

sideinfluence = SideInfluence.as_view('sideinfluence')
sideanalyst = SideAnalyst.as_view('sideanalyst')

site.add_url_rule('/influence/<int:page>', view_func=sideinfluence)
site.add_url_rule('/analyst/<int:page>', view_func=sideanalyst)


def init_app(app):
    app.register_blueprint(site)