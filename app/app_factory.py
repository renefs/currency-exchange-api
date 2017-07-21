from flask import Flask

from app.api.v1 import api_v1_bp
from app.api.v1.base import API_VERSION_V1
from app.extensions import db, api
from flask_migrate import Migrate


def create_app(config):
    application = Flask(__name__)
    application.config.from_object(config)

    application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    application.jinja_env.add_extension('jinja2.ext.do')

    db.init_app(app=application)
    api.init_app(app=application)

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    migrate = Migrate(application, db)

    _load_application_blueprints(application)

    _load_api_blueprints(application)

    _register_global_variables(application)

    return application


def _register_global_variables(application):
    @application.context_processor
    def inject_application_data():
        return dict(global_app_name=application.config.get('APP_NAME', 'TO DO'))


def _load_application_blueprints(application):
    from app.views.common import common_bp
    application.register_blueprint(common_bp)


def _load_api_blueprints(application):
    application.register_blueprint(api_v1_bp, url_prefix='{prefix}/v{version}'.format(
            prefix=application.config['API_URL_PREFIX'],
            version=API_VERSION_V1))
