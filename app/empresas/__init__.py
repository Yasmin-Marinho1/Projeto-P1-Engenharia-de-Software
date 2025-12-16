from flask import Blueprint

# Cria a blueprint 'empresa'
empresa_bp = Blueprint('empresa', __name__, template_folder='templates')

# Importa as rotas da pasta 'empresas'
from . import routes