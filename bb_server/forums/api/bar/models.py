from flask_auth.models import ModelMixin
from forums.extension import db
from forums.api.user.models import User
from datetime import datetime


class Bar(db.Model, ModelMixin):
    __tablename__ = 'bar'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer)
    title = db.Column(db.String(81), nullable=False)
    subtitle = db.Column(db.String(81))
    picture = db.Column(db.String(512), nullable=False)

class Questions(db.Model, ModelMixin):
    __tablename__ = 'questions'

    CONTENT_TYPE_TEXT = '0'
    CONTENT_TYPE_MARKDOWN = '1'
    CONTENT_TYPE_ORGMODE = '2'

    CONTENT_TYPE = (('0', 'text'), ('1', 'markdown'), ('2', 'org-mode'))

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(81), nullable=False)
    content = db.Column(db.Text, nullable=False)
    content_type = db.Column(
        db.String(10), nullable=False, default=CONTENT_TYPE_MARKDOWN)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())
    is_good = db.Column(db.Integer, default=0, nullable=False)
    is_bad = db.Column(db.Integer, default=0, nullable=False)
    bar_id = db.Column(db.Integer, nullable=False, default=0)
    is_bar = db.Column(db.SmallInteger,  default=0)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship(
        User, backref=db.backref(
            'user', lazy='dynamic'), lazy='joined')

class Answers(db.Model, ModelMixin):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    is_good = db.Column(db.Integer, default=0, nullable=False)
    is_bad = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())
    questions_id = db.Column(db.Integer)
    is_reply = db.Column(db.SmallInteger, default=0)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship(
        User, backref=db.backref(
            'bar_replies', lazy='dynamic'), lazy='joined')
  
class Comments(db.Model, ModelMixin):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    is_good = db.Column(db.Integer, default=0, nullable=False)
    is_bad = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())
    answers_id = db.Column(db.Integer)
    author_id = db.Column(db.Integer)

class Replys(db.Model, ModelMixin):
    __tablename__ = 'comment_replies'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    is_good = db.Column(db.Integer, default=0, nullable=False)
    is_bad = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())
    comments_id = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, nullable=False)
        