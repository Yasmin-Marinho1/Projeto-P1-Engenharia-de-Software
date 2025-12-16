from flask import Flask, url_for, session, flash, render_template, redirect, request
import csv

# Inicializa aa aplicação Flask
app = Flask(__name__)

# Chave secreta de sessões
app.secret_key = 'chave-secreta-aqui'

# Importando as blueprints

from app.usuario_comum import user_bp
from app.empresas import empresa_bp

# Registrando as blueprints na aplicação
app.register_blueprint(user_bp)
app.register_blueprint(empresa_bp, url_prefix='/empresas')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/cadastro")
def cadastro():
    """
    lógica da página de cadastro
    """
    return render_template('cadastro.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    """
    Rota GET/POST /login
    Exibe o formulário e processa autenticação
    """
    if request.method == 'GET':
        # Caso já esteja logado
        if session['user_role'] == 'user' or session['user_role'] == 'empresa':
            return redirect(url_for('index'))
        else:
            return render_template('login.html')
    elif request.method ==  'POST':
        cpf = request.form.get('cpf')
        cnpj = request.form.get('cnpj')
        senha =  request.form.get('senha')
        
        # Quando enviar o form como usuário empresa
        if cpf == None and cnpj != None:
            with open('data/cadastro_dos_usuarios.csv', mode='r', encoding='utf-8') as arquivo_csv:
                # Armazena os dados em um dicionário
                leitor = csv.DictReader(arquivo_csv)

                # Passa por cada linha do dicionário
                for linha in leitor:
                    # Caso ache o CNPJ
                    if linha.get('cnpj') == cnpj:
                        # Verifica se a senha corresponde e, se sim, procede login
                        if linha.get('senha') == senha:
                            flash(f'Login bem sucedido, bem vinda, {linha.get('nome')}!', 'success')
                            session['user_role'] = 'empresa'
                            return redirect(url_for('index'))
                        else:
                            break
                # Caso não ache ou senha não corresponda, exibe mensagem de erro
                flash('CNPJ ou senha incorretos.', 'error')

        # Quando enviar o form como usuário comum
        elif cpf != None and cnpj == None:
            with open('data/cadastro_dos_usuarios.csv', mode='r', encoding='utf-8') as arquivo_csv:
                # Armazena os dados em um dicionário
                leitor = csv.DictReader(arquivo_csv)
                for linha in leitor:
                    # Caso ache o CPF
                    if linha.get('cpf') == cpf:
                        # Verifica se a senha corresponde e, se sim, procede login
                        if linha.get('senha') == senha:
                            flash(f'Login bem sucedido, bem vindo(a), {linha.get('nome')}!', 'success')
                            session['user_role'] = 'user'
                            return redirect(url_for('index'))
                        else:
                            break
                # Caso não ache ou senha não corresponda, exibe mensagem de erro
                flash('CPF ou senha incorretos.', 'error')
        else:
            flash('Digite um CPF/CNPJ válido', 'error')


# Ponto de entrada da aplicação
if __name__ == '__main__':
    app.run(debug=True)