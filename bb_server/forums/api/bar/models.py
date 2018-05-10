from flask_auth.models import ModelMixin
from forums.extension import db
from forums.api.user.models import User
from datetime import datetime


class Bar(db.Model, ModelMixin):
    __tablename__ = 'bar'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(
        db.Integer, db.ForeignKey(
            'user.id', ondelete="CASCADE"))
    author = db.relationship(
        User,
        backref=db.backref(
            'bars', cascade='all,delete-orphan', lazy='dynamic'),
        lazy='joined')
    title = db.Column(db.String(255), nullable=False)
    subtitle = db.Column(db.String(255))
    picture = db.Column(db.String(512), nullable=False)

    def __repr__(self):
        return self.title

class Questions(db.Model, ModelMixin):
    __tablename__ = 'questions'

    CONTENT_TYPE_TEXT = '0'
    CONTENT_TYPE_MARKDOWN = '1'
    CONTENT_TYPE_ORGMODE = '2'

    CONTENT_TYPE = (('0', 'text'), ('1', 'markdown'), ('2', 'org-mode'))

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    content_type = db.Column(
        db.String(10), nullable=False, default=CONTENT_TYPE_MARKDOWN)
    created_at = db.Column(
        db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)
    is_good = db.Column(db.String(512), default='[]')
    is_bad = db.Column(db.String(512), default='[]')
    bar_id = db.Column(db.Integer, 
                db.ForeignKey('bar.id', ondelete="CASCADE"), nullable=False, default=0,)
    bar = db.relationship(
        Bar,
        backref=db.backref(
            'bar-questions', cascade='all,delete-orphan', lazy='dynamic'),
        lazy='joined')

    is_bar = db.Column(db.SmallInteger,  default=0)
    author_id = db.Column(
        db.Integer, db.ForeignKey(
            'user.id', ondelete="CASCADE"))
    author = db.relationship(
        User,
        backref=db.backref(
            'questions', cascade='all,delete-orphan', lazy='dynamic'),
        lazy='joined')

class Answers(db.Model, ModelMixin):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    is_good = db.Column(db.String(512), default='[]')
    is_bad = db.Column(db.String(512), default='[]')
    created_at = db.Column(
        db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)
    questions_id = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete="CASCADE"))
    question = db.relationship(
        Questions, backref=db.backref(
            'question', cascade='all,delete-orphan',lazy='dynamic'), lazy='joined')
    is_reply = db.Column(db.SmallInteger, default=0)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))
    author = db.relationship(
        User, backref=db.backref(
            'answers', cascade='all,delete-orphan',lazy='dynamic'), lazy='joined')
  
class Comments(db.Model, ModelMixin):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    is_good = db.Column(db.String(512), default='[]')
    is_bad = db.Column(db.String(512), default='[]')
    created_at = db.Column(
        db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)
    answers_id = db.Column(db.Integer, db.ForeignKey(
            'answers.id', ondelete="CASCADE"))
    answer = db.relationship(
        Answers, backref=db.backref(
            'answer', cascade='all,delete-orphan', lazy='dynamic'), lazy='joined')
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))
    author = db.relationship(
        User, backref=db.backref(
            'comments', cascade='all,delete-orphan', lazy='dynamic'), lazy='joined')

    reference = db.Column(db.String(512))
    at_user = db.Column(db.String(81))


'''class Replys(db.Model, ModelMixin):
    __tablename__ = 'comment_replies'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    is_good = db.Column(db.Integer, default=0, nullable=False)
    is_bad = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)
    comments_id = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, nullable=False)
'''