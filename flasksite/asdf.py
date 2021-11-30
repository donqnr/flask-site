import click
from flask import current_app, g
from flask.cli import with_appcontext
from flasksite import db

def init_db():
    db.init_app(current_app)
    db.drop_all()
    db.create_all()

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

@click.command('add-admin')
@with_appcontext
def add_admin():
    click.echo('stuff')

def init_app(app):
    app.cli.add_command(init_db_command)
    app.cli.add_command(add_admin)