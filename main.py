from flask import Flask, url_for, session, flash, render_template, redirect, request
import csv
import os
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()

# Inicializa aa aplicação Flask
app = Flask(__name__)

# Busca a chave do ambiente, com um valor padrão caso não encontre
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-padrao')

# Importando as blueprints
from app.usuario_comum import user_bp
from app.empresas import empresa_bp

# Caminho para arquivos de dados
data_dir =  'data'
cadastro_file = os.path.join(data_dir, 'cadastro_dos_usuarios.csv')
respostas_file = os.path.join(data_dir, 'respostas_questionario.csv')

# Cria a pasta data se ela não existe
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Vai garatir o cabeçalho correto para ambos os arquivos csv
if not os.path.exists(cadastro_file):
    with open(cadastro_file, mode='w', encoding='utf-8', newline='') as arquivo_csv:
        campos = ['cpf', 'nome','cnpj','nome_empresa','senha']
        escrever = csv.DictWriter(arquivo_csv, fieldnames=campos, delimiter=';')
        escrever.writeheader()

if not os.path.exists(respostas_file):
    with open(respostas_file, mode='w', encoding='utf-8', newline='') as arquivo_csv:
        campos = ['data', 'idade', 'genero', 'renda', 'estado', 'emissao', 'pontuacao']
        escrever = csv.DictWriter(arquivo_csv, fieldnames=campos, delimiter=';')
        escrever.writeheader()

# Registrando as blueprints na aplicação
app.register_blueprint(user_bp)
app.register_blueprint(empresa_bp, url_prefix='/empresas')

@app.route("/")
def index():
    """
    Rota GET /index
    Exibe a página inicial
    """
    return render_template('index.html')

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    """
    Rota GET/POST /cadastro
    Exibe o formulário e processa as informações
    """
    if request.method == 'POST':
        """
        Vai testar se o CPF/CNPJ está cadastrado, se estiver, redireciona para página de login
        Se não estiver, salva as informações de cadastro e redireciona para página de login
        """

        # Abre como 'reader' e verifica se o usuário está cadastrado
        with open(cadastro_file, mode='r', encoding='utf-8') as arquivo_csv:
            leitor = csv.DictReader(arquivo_csv, delimiter=';')
            cpf = request.form.get('cpf')
            cnpj = request.form.get('cnpj')
            if cnpj and not cpf:
                for linha in leitor:
                    # Procura se o CNPJ já está cadastrado
                    if linha.get('cnpj') == cnpj:
                        # Se estiver, redireciona para página de login
                        flash('CNPJ já cadastrado!', 'error')
                        return redirect(url_for('login'))
            elif cpf and not cnpj:
                for linha in leitor:
                    # Procura se o CPF já está cadastrado
                    if linha.get('cpf') == cpf:
                        # Se estiver, redireciona para página de login
                        flash('CPF já cadastrado!', 'error')
                        return redirect(url_for('login'))
                            
        # Se não estiver cadastrado, abre como 'append' e adiciona as informações
        campos = ['cpf', 'nome','cnpj','nome_empresa','senha']
        with open(cadastro_file, mode='a',  encoding='utf-8', newline='') as arquivo_csv:
            escrever = csv.DictWriter(arquivo_csv, fieldnames=campos, delimiter=';')
            # Explicitamente extrai os dados para garantir a ordem e evitar campos extras indesejados
            dados_usuario = {
                'cpf': request.form.get('cpf', ''),
                'nome': request.form.get('nome', ''),
                'cnpj': request.form.get('cnpj', ''),
                'nome_empresa': request.form.get('nome_empresa', ''),
                'senha': request.form.get('senha')
            }
            escrever.writerow(dados_usuario)
        flash('Cadastro realizado com sucesso! Faça seu  login', 'success')
        return redirect(url_for('login'))
    
    return render_template('cadastro.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    """
    Rota GET/POST /login
    Exibe o formulário e processa autenticação
    """
    if request.method == 'GET':
        # Caso já esteja logado
        if 'user_role' in session:
            return redirect(url_for('index'))
        else:
            return render_template('login.html')
    elif request.method ==  'POST':
        cpf = request.form.get('cpf')
        cnpj = request.form.get('cnpj')
        senha =  request.form.get('senha')
        
        # Quando enviar o form como usuário empresa (CNPJ preenchido, CPF vazio)
        if not cpf and cnpj:
            with open(cadastro_file, mode='r', encoding='utf-8') as arquivo_csv:
                # Armazena os dados em um dicionário
                leitor = csv.DictReader(arquivo_csv, delimiter=';')

                # Passa por cada linha do dicionário
                for linha in leitor:
                    # Caso ache o CNPJ
                    if linha.get('cnpj') == cnpj:
                        # Verifica se a senha corresponde e, se sim, procede login
                        if linha.get('senha') == senha:
                            username = linha.get('nome_empresa') or linha.get('nome')
                            flash(f'Login bem sucedido, bem vindo(a) à página de empresas, {username}!', 'success')
                            session['user_role'] = 'empresa'
                            return redirect(url_for('empresa.dados'))
                        else:
                            break
            # Caso não ache ou senha não corresponda, exibe mensagem de erro
            flash('CNPJ ou senha incorretos.', 'error')
            return render_template('login.html')

        # Quando enviar o form como usuário comum (CPF preenchido, CNPJ vazio)
        elif cpf and not cnpj:
            with open(cadastro_file, mode='r', encoding='utf-8') as arquivo_csv:
                # Armazena os dados em um dicionário
                leitor = csv.DictReader(arquivo_csv, delimiter=';')
                for linha in leitor:
                    # Caso ache o CPF
                    if linha.get('cpf') == cpf:
                        # Verifica se a senha corresponde e, se sim, procede login
                        if linha.get('senha') == senha:
                            username = linha.get('nome')
                            flash(f'Login bem sucedido, bem vindo(a) ao formulário, {username}!', 'success')
                            session['user_role'] = 'user'
                            return redirect(url_for('user.questionario'))
                        else:
                            break
            # Caso não ache ou senha não corresponda, exibe mensagem de erro
            flash('CPF ou senha incorretos.', 'error')
            return render_template('login.html')
        else:
            flash('Digite um CPF/CNPJ válido', 'error')


# Ponto de entrada da aplicação
if __name__ == '__main__':
    app.run(debug=True)