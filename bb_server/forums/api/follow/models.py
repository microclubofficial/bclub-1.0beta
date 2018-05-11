from flask_auth.models import ModelMixin
from forums.extension import db
from forums.api.user.models import User


class Follower(db.Model, ModelMixin):
    __tablename__ = 'followers'
    follwer = db.Column(db.String(512), nullable='[]')
    author_id = db.Column(
        db.Integer, db.ForeignKey(
            'user.id', ondelete="CASCADE"))
    author = db.relationship(
        User, backref=db.backref(
            'follower', cascade='all,delete-orphan', lazy='dynamic', passive_deletes=True), lazy='joined')