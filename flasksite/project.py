import re
import logging
import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flasksite import db, Project

bp = Blueprint('project', __name__, url_prefix='/project')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def get_project(p_id):
    proj = Project.query.filter_by(id=p_id).first()
    return proj

@bp.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        project_name = request.form['project_name']
        project_short_desc = request.form['project_short_desc']
        project_long_desc = request.form['project_long_desc']
        error = None

        if not project_name:
            error = 'Name required'

        if error is not None:
            flash(error)
        else:
            p = Project(project_name=project_name,project_short_desc=project_short_desc,project_long_desc=project_long_desc)
            db.session.add(p)
            db.session.commit()

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
