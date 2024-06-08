from flask import (Blueprint, url_for, render_template, g, request, redirect, flash)
from cobra.db import get_db
from cobra.auth import adm_required, login_required, logout_required

bp = Blueprint('adm', __name__, url_prefix='/adm')

@bp.route('/cidades')
@adm_required
def index_cidades():
    db = get_db()
    cidades = db.execute('SELECT * FROM cidade').fetchall()
    return render_template('adm/index_cidades.html', cidades = cidades)

@bp.route('/cidades/create', methods = ('GET', 'POST'))
@adm_required
def criar_cidade():
    if request.method == 'POST':
        nome = request.form['nome']
        promocao = request.form.get('promocao') or None
        error = None
        db = get_db()

        if not nome:
            error = 'Insira o nome da cidade'
        
        if error is None:
            try:
                db.execute('INSERT INTO cidade (nome, promocao_id) VALUES (?, ?)', (nome, promocao))
                db.commit()
            except db.IntegrityError:
                error = f"{nome} já estava registrado(a)."
            else:
                return redirect(url_for('adm.index_cidades'))
        flash(error)
    promocoes = get_db().execute('SELECT * FROM promocao').fetchall()
    return render_template('adm/create_cidade.html', promocoes = promocoes)


@bp.route('/promocoes')
@adm_required
def index_promocoes():
    db = get_db()
    promocoes = db.execute('SELECT * FROM promocao').fetchall()
    return render_template('adm/index_promocoes.html', promocoes = promocoes)

@bp.route('/promocoes/create', methods = ('GET', 'POST'))
@adm_required
def criar_promocao():
    if request.method == 'POST':
        nome = request.form['nome']
        desconto = int(request.form['desconto']) 
        error = None
        db = get_db()

        if not nome:
            error = 'Insira um nome para a promoção.'
        elif not desconto or desconto < 1 or desconto > 100:
            error = 'Insira um inteiro entre 1 e 100.'
        
        if error is None:
            try:
                db.execute(
                    'INSERT INTO promocao (nome, desconto, ativo) '
                    'VALUES (?, ?, 1)',
                    (nome, desconto)
                )
                db.commit()
            except db.IntegrityError as e:
                error = f"{e} já estava registrada."
            else:
                return redirect(url_for('adm.index_promocoes'))
        
        flash(error)
    return render_template('adm/create_promocao.html')