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
        name = request.form['name']
        description = request.form['description']
        image = request.form['image']
        advantages = request.form['advantages']
        disadvantages = request.form['disadvantages']

        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO gear (name, advantages, description,disadvantages, image, author_id)'
                ' VALUES (?,?,?,?,?,? )',
                (name, advantages, description, disadvantages, image, g.user['id'])
            )
            db.commit()
            return redirect(url_for('gears.index'))

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
        '''SELECT * FROM gear WHERE id = ?''',(id,)
    ).fetchall()
    return render_template('gear/detail.html', gear=gear, posts = posts)


#update gear template
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_gear(id)

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        image = request.form['image']
        advantages = request.form['advantages']
        disadvantages = request.form['disadvantages']

        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO gear (name, advantages, description,disadvantages, image, author_id)'
                ' VALUES (?,?,?,?,?,? )',
                (name, advantages, description, disadvantages, image, g.user['id'])
            )
            db.commit()
            return redirect(url_for('gears.index'))

    return render_template('gear/update.html', post=post)

#delete gear by id
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_gear(id)
    db = get_db()
    db.execute('DELETE FROM gear WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('gears.index'))