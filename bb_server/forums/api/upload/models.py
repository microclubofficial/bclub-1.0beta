from flask_auth.models import ModelMixin
from forums.extension import db

class Photo(db.Model, ModelMixin):
    __tablename__ = 'photos'

    id = db.Column(db.Integer, primary_key=True)
    front_photo = db.Column(db.String(512), nullable=False)
    photo_url = db.Column(db.String(512), nullable=False)
