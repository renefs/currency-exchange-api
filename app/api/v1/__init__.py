from flask import Blueprint
import flask_restful

from app.api.v1.exchange import ExchangeApi
from app.api.v1.hello import HelloWorld

api_v1_bp = Blueprint('api_v1', __name__)
api_v1 = flask_restful.Api(api_v1_bp)

api_v1.add_resource(HelloWorld, '/hello')
api_v1.add_resource(ExchangeApi, '/exchange')


