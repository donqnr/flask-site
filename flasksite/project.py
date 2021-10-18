import re
import logging
import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flasksite.db import get_db

bp = Blueprint('project', __name__, url_prefix='/project')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def get_project(id):
    proj = get_db().execute(
        'SELECT id, project_name, project_description FROM project'
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    return proj

@bp.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        project_name = request.form['project_name']
        project_description = request.form['project_description']
        error = None

        if not project_name:
            error = 'Name required'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO project (project_name, project_description)'
                ' VALUES (?, ?)',
                (project_name, project_description)
            )
            db.commit()

            return redirect(url_for('index.index'))
    
    return render_template('project/add.html')

@bp.route('/<int:id>')
def view(id):
    images = []
    try:
        images = os.listdir('flasksite/static/images/' + str(id))
    except FileNotFoundError:
        pass

    proj = get_project(id)

    if not proj:
        flash('No project found by that id')

    return render_template('project/view.html', proj=proj, images=images)
