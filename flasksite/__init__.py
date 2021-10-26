import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin

db = SQLAlchemy()

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(60))
    project_short_desc = db.Column(db.String(120))
    project_long_desc = db.Column(db.Text)
    links = db.relationship('Link', backref='project', lazy=True)
    def __repr__(self):
        return '<Project %r>' % self.project_name

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link_address = db.Column(db.Text)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flasksite.sqlite'),
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['FLASK_ADMIN_SWATCH'] = 'darkly'

    db.init_app(app)

    admin = Admin(app, name='fdsfdfds', template_mode='bootstrap3')
    admin.add_view(ModelView(Project, db.session, endpoint="projects"))
    admin.add_view(ModelView(Link, db.session, endpoint="links"))

    file_path = os.path.join(os.path.dirname(__file__), 'static')
    fileadmin_args = FileAdmin(file_path, '/static/', name='flsefisfd')
    fileadmin_args.allowed_extensions = ['png', 'jpg', 'gif']
    admin.add_view(fileadmin_args)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
        
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import asdf
    asdf.init_app(app)

    from . import index
    app.register_blueprint(index.bp)
    app.add_url_rule('/', endpoint='index')

    from . import project
    app.register_blueprint(project.bp)

    #asdf

    return app