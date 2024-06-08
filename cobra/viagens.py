from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)
from werkzeug.exceptions import abort
from cobra.auth import login_required, logout_required
from cobra.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    cidades = db.execute(
        'SELECT * FROM cidade'
    ).fetchall()
    return render_template('viagens/index.html', cidades = cidades)