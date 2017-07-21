import flask_restful
from marshmallow_jsonapi import Schema, fields

class HelloWorldSchema(Schema):
    id = fields.Str(dump_only=True)
    hello = fields.String()
    version = fields.Integer()

    class Meta:
        type_ = 'hello_world'


from app.api.v1.base import API_VERSION


class HelloWorld(flask_restful.Resource):
    def get(self):
        api_info = dict(hello='world', version=API_VERSION)
        schema = HelloWorldSchema()
        result = schema.dump(api_info)
        return result
