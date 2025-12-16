from flask import Flask, url_for, session, flash, render_template, redirect

# Inicializa aa aplicação Flask
app = Flask(__name__)

# Chave secreta de sessões
app.secret_key = 'chave-secreta-aqui'

# Importando as blueprints

from app.usuario_comum import user_bp
from app.empresas import empresa_bp

# Registrando as blueprints na aplicação
app.register_blueprint(user_bp)
app.register_blueprint(empresa_bp, url_prefix='/empresa')

@app.route("/")
def index():
    """
    lógica da página index
    """
    return render_template('index.html')

@app.route("/cadastro")
def cadastro():
    """
    lógica da página de cadastro
    """
    return render_template('cadastro.html')

@app.route("/login")
def login():
    """
    lógica da página de login
    """
    return render_template('login.html')

# Ponto de entrada da aplicação
if __name__ == '__main__':
    app.run(debug=True)