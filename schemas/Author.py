from ma import ma
from models.Author import AuthorModel
from models.Article import ArticleModel
from schemas.Article import ArticleSchema


class AuthorSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = AuthorModel
        load_instance = True
        include_fk = True