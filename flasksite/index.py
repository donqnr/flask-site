from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from flasksite import db, Project

bp = Blueprint('index', __name__)

@bp.route('/')
def index():
    projs = Project.query.all()

    return render_template('index.html', projs=projs)

def get_project(id):
    proj = None

    if proj is None:
        abort(404, f"Project id {id} not found.")

    return proj