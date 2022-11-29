from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from flaskr.auth import login_required
from flaskr.db import get_db
from flask import Flask,render_template,request
import os
bp = Blueprint('gears', __name__)

@bp.route('/propos')
def propos():
    return render_template('propos.html')