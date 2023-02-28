from ma import ma
from models.PageCount import PAgeCount
from marshmallow import Schema, fields

class PageCountSchema(Schema):
    pagecount = fields.Integer()