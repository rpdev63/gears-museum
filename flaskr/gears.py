from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db
bp = Blueprint('gears', __name__)


#show all gears
@bp.route('/')
def index():
    db = get_db()
    gears = db.execute(
        'SELECT g.id as gid, name, created_at, author_id, u.username as username'
        ' FROM gear g JOIN user u ON g.author_id = u.id'
        ' ORDER BY created_at DESC'
    ).fetchall()
    return render_template('gear/index.html', gears=gears)

#create gear template
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('gear.index'))

    return render_template('gear/create.html')

#select gear by id
def get_gear(id):
    gear = get_db().execute(
        'SELECT * '
        ' FROM gear g WHERE g.id = ?',
        (id,)
    ).fetchone()

    if gear is None:
        abort(404, f"Post id {id} doesn't exist.")

    return gear
       
@bp.route('/<int:id>/detail')
def display_one(id):
    gear = get_gear(id)
    posts = get_db().execute(
        '''SELECT * FROM post WHERE gear_id = ?''',(id,)
    ).fetchall()
    return render_template('gear/detail.html', gear=gear, posts = posts)


#update gear template
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_gear(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('gear.index'))

    return render_template('gear/update.html', post=post)

#delete gear by id
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_gear(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('gear.index'))

import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/image'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return