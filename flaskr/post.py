from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
bp = Blueprint('post', __name__, url_prefix='/post')

#show all posts
@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created_at, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created_at DESC'
    ).fetchall()
    return render_template('post/index.html', posts=posts)

#create post template 
@bp.route('/<int:id>/create', methods=('GET', 'POST'))
@login_required
def create(id):
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        gear_id = id
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, gear_id, author_id)'
                ' VALUES (?, ?, ?, ?)',
                (title, body, gear_id, g.user['id'])
            )
            db.commit()
            return redirect(url_for('gears.display_one', id=id))

    return render_template('post/create.html')

#select post by ID
def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created_at, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

#update post template
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

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
            return redirect(url_for('gears.index'))

    return render_template('post/update.html', post=post)

#delete
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('post.index'))