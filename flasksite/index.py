from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from flasksite.db import get_db

bp = Blueprint('index', __name__)

@bp.route('/')
def index():
    db = get_db()
    projs = db.execute(
        'SELECT id, project_name, project_description FROM project'
    ).fetchall()

    return render_template('index.html', projs=projs)

def get_project(id):
    proj = get_db().execute(
        'SELECT id, project_name, project_description'
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if proj is None:
        abort(404, f"Project id {id} not found.")

    return proj