import click

from app.extensions import db


def initialize_cli(app):
    @app.cli.command()
    def init_db():
        """Initialize the database."""
        click.echo('Initializing the db')
        db.create_all()

    @app.cli.command()
    def clear_db():
        """Initialize the database."""
        click.echo('Clearing the db')
        db.drop_all()
        click.echo('Initializing the db')
        db.create_all()
