from app.app_factory import create_app
from app.cli import initialize_cli
from app.config import BaseConfig

application= create_app(BaseConfig)

initialize_cli(application)
