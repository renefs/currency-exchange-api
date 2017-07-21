from datetime import datetime

import flask_restful
import requests
from flask_restful import reqparse
from marshmallow_jsonapi import Schema, fields
from sqlalchemy.orm.exc import NoResultFound

from app.api.v1.base import API_VERSION
from flask import current_app

from app.extensions import db
from app.models import Exchange


class ExchangeSchema(Schema):
    id = fields.Str(dump_only=True)
    currency_from = fields.String()
    currency_to = fields.String()
    date = fields.Date()
    value = fields.String()

    class Meta:
        type_ = 'currency_exchange'


class ExchangeApi(flask_restful.Resource):
    def __init__(self):
        """
            Initializes the class instance with a request parser validator.
            The class requires a browser_name and a browser_vesion.
        :return: The class instance
        """
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('from', type=str, required=True,
                                   help='No source currency provided', location='args')
        self.reqparse.add_argument('to', type=str, required=True,
                                   help='No destiny currency provided', location='args')
        super(ExchangeApi, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()

        currency_from = args.get('from')
        currency_to = args.get('to')

        try:
            db_exchange = Exchange.query.filter_by(currency_from=currency_from, currency_to=currency_to).one()
            value = db_exchange.value
            date = db_exchange.date

            if date < datetime.today():
                value, date = self.get_exchange_from_3rd_party(currency_from, currency_to)

        except NoResultFound:

            value, date = self.get_exchange_from_3rd_party(currency_from, currency_to)
            current_app.logger.debug('{} - {}'.format(value, date))

        api_info = dict(currency_from=currency_from,
                        currency_to=currency_to,
                        value=value,
                        date=date,
                        version=API_VERSION)

        schema = ExchangeSchema()
        result = schema.dump(api_info)
        return result

    @staticmethod
    def get_exchange_from_3rd_party(currency_from, currency_to):
        request = requests.get('http://api.fixer.io/latest?base={}'.format(currency_from))
        result = request.json()
        current_app.logger.debug(result)

        ExchangeApi.save_new_exchange(currency_from, currency_to, result)

        return result['rates'][currency_to], datetime.strptime(result['date'], '%Y-%m-%d')

    @staticmethod
    def save_new_exchange(currency_from, currency_to, result):

        try:
            db_exchange = Exchange.query.filter_by(currency_from=currency_from, currency_to=currency_to).one()
            db_exchange.currency_from = currency_from
            db_exchange.currency_to = currency_to
            db_exchange.value = result['rates'][currency_to]
            db_exchange.date = datetime.strptime(result['date'], '%Y-%m-%d')
        except NoResultFound:
            db.session.add(Exchange(currency_from=currency_from,
                                    currency_to=currency_to,
                                    value=result['rates'][currency_to],
                                    date=datetime.strptime(result['date'], '%Y-%m-%d')
                                    )
                           )
        db.session.commit()
