from flask import Flask, Blueprint, jsonify
from flask_restplus import Api
from flask_cors import CORS
from auth.views import auth_blueprint
from flask_bcrypt import Bcrypt
from ma import ma
from db import db


from resources.Author import Author, AuthorList, author_ns, authors_ns
from resources.Article import Article, ArticleList,ArticlePagination,ArticlePaginationSearch,ArticlePaginationPages,ArticlePaginationSearchPages,ArticlePaginationPages,  articles_ns, article_ns, article_pagination_ns, article_pagination_search_ns, article_pagination_pages_ns, article_pagination_search_pages_ns
from resources.User import User,UserList,user_ns,users_ns
from marshmallow import ValidationError

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)
app.register_blueprint(auth_blueprint)

bluePrint = Blueprint('api', __name__, url_prefix='/api')
api = Api(bluePrint, doc='/doc', title='Article backend application')
app.register_blueprint(bluePrint)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

api.add_namespace(article_ns)
api.add_namespace(articles_ns)
api.add_namespace(article_pagination_ns)
api.add_namespace(article_pagination_search_ns)
api.add_namespace(article_pagination_pages_ns)
api.add_namespace(article_pagination_search_pages_ns)
api.add_namespace(author_ns)
api.add_namespace(authors_ns)
api.add_namespace(user_ns)
api.add_namespace(users_ns)


@app.before_first_request
def create_tables():
    db.create_all()


@api.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400


article_ns.add_resource(Article, '/<int:id>')
articles_ns.add_resource(ArticleList, "")
author_ns.add_resource(Author, '/<int:id>')
authors_ns.add_resource(AuthorList, "")
article_pagination_ns.add_resource(ArticlePagination, '/<int:page>/<int:limit>')
article_pagination_pages_ns.add_resource(ArticlePaginationPages, '/<int:page>/<int:limit>')
article_pagination_search_ns.add_resource(ArticlePaginationSearch, '/<int:page>/<int:limit>/<string:value>')
article_pagination_search_pages_ns.add_resource(ArticlePaginationSearchPages, '/<int:page>/<int:limit>/<string:value>')
user_ns.add_resource(User, '/<int:id>')
users_ns.add_resource(UserList, "")

if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5022, debug=True)

 