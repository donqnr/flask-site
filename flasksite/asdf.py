import click
from flask import current_app, g
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash
from flasksite import db, User

def init_db():
    db.init_app(current_app)
    db.drop_all()
    db.create_all()

@click.command('create-all')
@with_appcontext
def create_all_command():
    db.create_all()
    click.echo('hjkjj')

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

@click.command('add-admin')
@click.argument('user')
@click.argument('pword')
@with_appcontext
def add_admin(user, pword):
    newuser = User(login=user,password=generate_password_hash(pword))
    db.session.add(newuser)
    db.session.commit()
    click.echo("User " + user + " added")

def init_app(app):
    
    app.cli.add_command(init_db_command)
    app.cli.add_command(add_admin)