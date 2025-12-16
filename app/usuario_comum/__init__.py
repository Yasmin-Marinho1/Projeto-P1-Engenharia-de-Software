from flask import Blueprint

# Criando o blueprint "user"
user_bp = Blueprint('user', __name__, template_folder='templates')

# Importando as rotas da pasta usuario_comum
from . import routes