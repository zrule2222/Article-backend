from db import db
from typing import List
from sqlalchemy.sql import func
from flask_sqlalchemy import Pagination



class ArticleModel(db.Model):
    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    body = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(db.DateTime, onupdate=func.now())

    author =db.Column(db.Integer,db.ForeignKey('authors.id'),nullable=False)
    author_relation = db.relationship("AuthorModel",)

    def __init__(self, title, body, author,created_at = func.now(),updated_at = func.now()):
        self.title = title
        self.body = body
        self.created_at = created_at
        self.updated_at = updated_at
        self.author = author

    def __repr__(self):
        return 'ArticleModel(title=%s, body=%s,author_id=%s,created_at=%s,updated_at=%s)' % (self.title, self.body,self.author_id,self.created_at,self.updated_at)

    def json(self):
        return {'title': self.title, 'body': self.body, 'created_at': self.created_at, 'updated_at': self.updated_at}

    @classmethod
    def find_by_title(cls, title) -> "ArticleModel":
        return cls.query.filter_by(title=title).first()

    @classmethod
    def find_by_id(cls, _id) -> "ArticleModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["ArticleModel"]:
        return cls.query.all()

    @classmethod
    def get_paginated(cls,page,limit) -> List["ArticleModel"]:
            return cls.query.paginate(page, per_page=limit)
    
    @classmethod
    def get_paginated_search(cls,page,limit,value) -> "ArticleModel":
         return cls.query.filter(cls.title.like((f'%{value}%')) | cls.body.like(f'%{value}%') | cls.created_at.like(f'%{value}%') | cls.updated_at.like(f'%{value}%')).paginate(page, per_page=limit)

    


    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()