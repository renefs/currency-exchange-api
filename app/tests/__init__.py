# -*- coding: utf-8 -*-
import os
from flask_testing import TestCase
from flask import request
from app.app_factory import create_app
from app.extensions import db

_basedir = os.path.abspath(os.path.dirname(__file__))


class BaseTestCase(TestCase):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'test_app.db')
    TESTING = True
    WTF_CSRF_ENABLED = False
    WTF_CSRF_SECRET_KEY = "somethingimpossibletoguess"
    SECRET_KEY = 'This string will be replaced with a proper key in production.'
    APPLICATION_ROOT = "/"
    API_URL_PREFIX = "/api"

    IS_LOCAL_INSTALLATION = True

    # available languages
    LANGUAGES = {
        'en': 'English',
        'es': 'Español'
    }

    def create_app(self):

        application = create_app(self)

        return application

    def setUp(self):
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()