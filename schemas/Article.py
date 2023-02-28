from ma import ma
from models.Article import ArticleModel
from models.Author import AuthorModel


class ArticleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ArticleModel
        load_instance = True
        load_only = ("author_relation",)
        include_fk= True