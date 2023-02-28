from db import db
from typing import List
import datetime
from sqlalchemy.sql import func


class AuthorModel(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(db.DateTime, onupdate=func.now())

    articles = db.relationship("ArticleModel",lazy="dynamic",primaryjoin="AuthorModel.id == ArticleModel.author")
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'StoreModel(name=%s, created_at=%s, updated_at=%s)' % (self.name, self.created_at, self.updated_at)

    @classmethod
    def find_by_name(cls, name) -> "AuthorModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id) -> "AuthorModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["AuthorModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()