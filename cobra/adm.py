from flask import (Blueprint, url_for, render_template, g, request, redirect, flash)
from cobra.db import get_db
from cobra.auth import adm_required, login_required, logout_required

bp = Blueprint('adm', __name__, url_prefix='/adm')

@bp.route('/')
@adm_required
def index():
    db = get_db()
    cidades = db.execute('SELECT * FROM cidade').fetchall()
    promocoes = db.execute('SELECT * FROM promocao').fetchall()
    return render_template('adm/index.html', cidades = cidades, promocoes = promocoes)

@bp.route('/cidades/create', methods = ('GET', 'POST'))
@adm_required
def criar_cidade():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        preco = int(request.form['preco'])
        promocao = request.form.get('promocao') or None
        error = None
        db = get_db()

        if not nome:
            error = 'Insira o nome da cidade'
        
        if error is None:
            try:
                db.execute('INSERT INTO cidade (nome, descricao, preco, promocao_id) VALUES (?, ?, ?, ?)', (nome, descricao, preco, promocao))
                db.commit()
            except db.IntegrityError:
                error = f"{nome} já estava registrado(a)."
            else:
                return redirect(url_for('adm.index'))
        flash(error)
    promocoes = get_db().execute('SELECT * FROM promocao').fetchall()
    return render_template('adm/create_cidade.html', promocoes = promocoes)



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
                return redirect(url_for('adm.index'))
        
        flash(error)
    return render_template('adm/create_promocao.html')