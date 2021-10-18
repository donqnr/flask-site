import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flasksite.sqlite'),
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    app.config['FLASK_ADMIN_SWATCH'] = 'darkly'
    db = SQLAlchemy(app)

    admin = Admin(app, name='shit', template_mode='bootstrap3')

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

    from . import db
    db.init_app(app)

    from . import index
    app.register_blueprint(index.bp)
    app.add_url_rule('/', endpoint='index')

    from . import project
    app.register_blueprint(project.bp)

    admin.add_view(ModelView(project, db.session))

    return app