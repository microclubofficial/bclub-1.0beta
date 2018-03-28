from flask_auth.models import ModelMixin
from forums.extension import db

class File(db.Model, ModelMixin):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    front_file = db.Column(db.String(512), nullable=False)
    file_path = db.Column(db.String(512), nullable=False)
