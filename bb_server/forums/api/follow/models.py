from flask_auth.models import ModelMixin
from forums.extension import db


class Follower(db.Model, ModelMixin):
    __tablename__ = 'followers'
    follwer = db.Column(db.String(512), nullable='[]')
    author_id = db.Column(
        db.Integer, db.ForeignKey(
            'user.id', ondelete="CASCADE"))