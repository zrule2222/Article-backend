from flask import request
from flask_restplus import Resource, fields, Namespace
from sqlalchemy.sql import func

from models.Article import ArticleModel
from schemas.Article import ArticleSchema

from models.PageCount import PAgeCount
from schemas.PageCount import PageCountSchema

ARTICLE_NOT_FOUND = "Article not found."


article_ns = Namespace('article', description='Article related operations')
articles_ns = Namespace('articles', description='Articles related operations')
article_pagination_ns = Namespace('articlePagination', description='Get paginated articles')
article_pagination_pages_ns = Namespace('articlePaginationPages', description='Get paginated articles')
article_pagination_search_ns = Namespace('articlePaginationSearch', description='Get paginated articles with a searched value')
article_pagination_search_pages_ns = Namespace('articlePaginationSearchPages', description='Get paginated articles')
article_schema = ArticleSchema()
article_list_schema = ArticleSchema(many=True)
page_count_schema = PageCountSchema()

#Model required by flask_restplus for expect
article = article_ns.model('Article', {
    'title': fields.String,
    'body': fields.String,
    'author': fields.Integer
})


class Article(Resource):

    def get(self, id):
        article_data = ArticleModel.find_by_id(id)
        if article_data:
            return article_schema.dump(article_data)
        return {'message': ARTICLE_NOT_FOUND}, 404

    def delete(self,id):
        article_data = ArticleModel.find_by_id(id)
        if article_data:
            article_data.delete_from_db()
            return {'message': "Article Deleted successfully"}, 200
        return {'message': ARTICLE_NOT_FOUND}, 404

    @article_ns.expect(article)
    def put(self, id):
        article_data = ArticleModel.find_by_id(id)
        article_json = request.get_json();

        if article_data:
            article_data.title = article_json['title']
            article_data.body = article_json['body']
            article_data.updated_at = func.now()
        else:
            article_data = article_schema.load(article_json)

        article_data.save_to_db()
        return article_schema.dump(article_data), 200




class ArticleList(Resource):
    @article_ns.doc('Get all the Articles')
    def get(self):
        return article_list_schema.dump(ArticleModel.find_all()), 200

    @article_ns.expect(article)
    @article_ns.doc('Create an Article')
    def post(self):
        article_json = request.get_json()
        article_data = article_schema.load(article_json)
        article_data.save_to_db()

        return article_schema.dump(article_data), 201

class ArticlePagination(Resource):
     @article_ns.doc('Get all the paginated Articles')
     def get(self,page,limit):
        return article_list_schema.dump(ArticleModel.get_paginated(page,limit).items), 200

class ArticlePaginationSearch(Resource):
     @article_ns.doc('Get all the paginated Articles with a spesific value')
     def get(self,page,limit,value):
        return article_list_schema.dump(ArticleModel.get_paginated_search(page,limit,value).items), 200

class ArticlePaginationPages(Resource):
     def get(self,page,limit):
       pagesc=PAgeCount(pagecount=ArticleModel.get_paginated(page,limit).pages)  
       return page_count_schema.dump(pagesc),200

class ArticlePaginationSearchPages(Resource):
    def get(self,page,limit,value):
        pagesc=PAgeCount(pagecount=ArticleModel.get_paginated_search(page,limit,value).pages)  
        return page_count_schema.dump(pagesc),200