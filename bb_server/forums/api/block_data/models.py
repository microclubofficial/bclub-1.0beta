from flask_auth.models import ModelMixin
from forums.extension import db

class B_Picture(db.Model, ModelMixin):
    __tablename__ = 'b_picture'
    id = db.Column(db.Integer, primary_key=True)
    picture = db.Column(db.String(81))
