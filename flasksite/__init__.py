import os
import re
from click.types import File

from flask import Flask, redirect, url_for, request
from flask_login.utils import logout_user
from flask_sqlalchemy import SQLAlchemy
import flask_admin as admin
from flask_admin import helpers, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from wtforms import form, fields, validators
from werkzeug.security import generate_password_hash, check_password_hash
import flask_login as login

db = SQLAlchemy()
login_manager = login.LoginManager()

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

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100))
    password = db.Column(db.String(100))

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)

class LoginForm(form.Form):
    login = fields.StringField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('no')

        if not check_password_hash(user.password, self.password.data):
            raise validators.ValidationError('no')

    def get_user(self):
        return db.session.query(User).filter_by(login=self.login.data).first()

class ProjectView(ModelView):

    def is_accessible(self):
        return login.current_user.is_authenticated

class NewFileAdmin(FileAdmin):

    def is_accessible(self):
        return login.current_user.is_authenticated

class AdminIndex(admin.AdminIndexView):
    @expose('/')
    def admin_index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login'))
        return super(AdminIndex, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login(self):
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)
        if login.current_user.is_authenticated:
            return redirect(url_for('.admin_index'))

        self._template_args['form'] = form
        return super(AdminIndex, self).index()

    @expose('/logout/')
    def logout(self):
        login.logout_user()
        return redirect(url_for('.login'))

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flasksite.sqlite'),
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databse.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['FLASK_ADMIN_SWATCH'] = 'darkly'

    db.init_app(app)

    login_manager.init_app(app)

    admn = admin.Admin(app, name='fdsfdfds', index_view=AdminIndex(), template_mode='bootstrap3')
    admn.add_view(ProjectView(Project, db.session,  endpoint="projects"))
    admn.add_view(ProjectView(Link, db.session,  endpoint="links"))

    file_path = os.path.join(os.path.dirname(__file__), 'static')
    fileadmin_args = NewFileAdmin(file_path, '/static/', name='flsefisfd')
    fileadmin_args.allowed_extensions = ['png', 'jpg', 'gif']
    admn.add_view(fileadmin_args)

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