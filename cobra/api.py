from flask import Blueprint
from cobra.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/')
def index():
    db = get_db()
    cidades = db.execute('SELECT * FROM cidade').fetchall()
    cidades_list = []
    for cidade in cidades:
        cidades_list.append(dictionarize(cidade))
    
    return cidades_list


def dictionarize(row):
    obj = {}
    for key in row.keys():
        obj[key] = row[key]
    return obj