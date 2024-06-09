from flask import Blueprint, request, render_template, redirect, flash, g, url_for
from cobra.db import get_db
from cobra.auth import login_required, logout_required

bp = Blueprint('tickets', __name__, url_prefix='/tickets')

@bp.route('/')
@login_required
def index():
    tickets = get_db().execute(
        'SELECT ticket.id, ticket.created, ticket.partida, origem.nome as origem_nome, destino.nome as destino_nome '
        'FROM ticket JOIN cidade origem ON ticket.origem_id = origem.id JOIN cidade destino ON ticket.destino_id = destino.id '
        'WHERE ticket.user_id = ?',
        (g.user['id'], )
    ).fetchall()
    return render_template('tickets/index.html', tickets = tickets)

@bp.route('/buy/<int:id>', methods = ('GET', 'POST'))
@login_required
def buy(id):
    db = get_db()

    if request.method == 'POST':
        from datetime import datetime, timedelta, timezone
        origem = int(request.form.get('origem'))
        user_id = g.user['id']
        partida = datetime.now(timezone.utc) + timedelta(days=1)
        partida = partida.isoformat(' ', 'seconds')[:-6]
        error = None

        if not origem:
            error = 'Por favor, especifique a origem da viagem.'
        
        if error is None:
            try:
                db.execute('INSERT INTO ticket(user_id, origem_id, destino_id, partida) VALUES (?, ?, ?, ?)', (user_id, origem, id, partida))
                db.commit()
            except db.IntegrityError:
                error = "Erro ao comprar passagem."
            else:
                return redirect(url_for('tickets.index'))
        flash(error)
    
    destino = db.execute('SELECT * FROM cidade WHERE id = ?', (id, )).fetchone()
    cidades = db.execute('SELECT * FROM cidade').fetchall()

    return render_template('tickets/buy.html', destino = destino, cidades = cidades)
