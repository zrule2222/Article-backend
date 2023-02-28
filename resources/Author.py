from flask import request
from flask_restplus import Resource, fields, Namespace

from models.Author import AuthorModel
from schemas.Author import AuthorSchema


AUTHOR_NOT_FOUND = "Authtor not found."
AUTHOR_ALREADY_EXISTS = "Author '{}' Already exists."

author_ns = Namespace('author', description='Author related operations')
authors_ns = Namespace('authors', description='Authors related operations')

author_schema = AuthorSchema()
author_list_schema = AuthorSchema(many=True)

# Model required by flask_restplus for expect
author = author_ns.model('Author', {
    'name': fields.String()
})


class Author(Resource):
    def get(self, id):
        author_data = AuthorModel.find_by_id(id)
        if author_data:
            return author_schema.dump(author_data)
        return {'message': AUTHOR_NOT_FOUND}, 404

    def delete(self, id):
        author_data = AuthorModel.find_by_id(id)
        if author_data:
            author_data.delete_from_db()
            return {'message': "Author Deleted successfully"}, 200
        return {'message': AUTHOR_NOT_FOUND}, 404


class AuthorList(Resource):

    @author_ns.doc('Get all the Authors')
    def get(self):
        return author_list_schema.dump(AuthorModel.find_all()), 200

    @author_ns.expect(author)
    @author_ns.doc('Create a Author')
    def post(self):
        author_json = request.get_json()
        print(author_json)
        name = author_json['name']
        if AuthorModel.find_by_name(name):
            return {'message': AUTHOR_ALREADY_EXISTS.format(name)}, 400
        author_data = author_schema.load(author_json)
        author_data.save_to_db()

        return author_schema.dump(author_data), 201