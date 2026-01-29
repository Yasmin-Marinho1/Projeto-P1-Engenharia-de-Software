from flask import render_template, request, redirect, url_for, session, flash
from datetime import datetime
from . import user_bp
import os
import csv


data_dir =  'data'
respostas_file = os.path.join(data_dir, 'respostas_questionario.csv')

@user_bp.route('/questionario', methods=['GET', 'POST'])
def questionario():
    '''
    Rota GET/POST /questionario
    Exibe o questionário e processa autenticação
    '''
    if request.method == 'POST':
        # Processa os dados do questionário aqui
        # Obtém data(dia/mês/ano) da resposta
        data_atual = datetime.now().strftime('%d/%m/%Y')
        
        campos = ['data', 'idade', 'genero', 'renda', 'estado', 'emissao', 'pontuacao']
        with open(respostas_file, mode='a',  encoding='utf-8', newline='') as arquivo_csv:
            escrever = csv.DictWriter(arquivo_csv, fieldnames=campos, delimiter=';')
            dados_respostas = {
                'data': data_atual,
                'idade': request.form.get('idade', ''),
                'genero': request.form.get('genero', ''),
                'renda': request.form.get('renda', ''),
                'estado': request.form.get('estado', ''),
                'emissao': request.form.get('emissao', ''),
                'pontuacao': request.form.get('pontuacao', '')
            }
            escrever.writerow(dados_respostas)
        flash('Obrigado por contribuir com suas respostas!', 'success')
        username = session.get('username')
        emissao = dados_respostas['emissao']
        pontuacao = int(dados_respostas['pontuacao'])
        return render_template('resultado.html', pontuacao=pontuacao, emissao=emissao)
    return render_template('questionario.html')

@user_bp.route('/resultados_questionario')
def resultados_questionario(pontuacao, emissao):
    '''
    Rota GET /resultados_questionario
    Exibe os resultados do questionário com base na pontuação
    '''
    # Se o usuário ainda não respondeu ao questionário, redireciona para o questionário
    if 'respondeu' not in session:
        flash('Por favor, responda ao questionário primeiro.', 'error')
        return redirect(url_for('user_bp.questionario'))
    username = session.get('username')
    emissao = request.args.get('emissao')
    pontuacao = int(request.args.get('pontuacao'))
    return render_template('resultados_questionario.html', pontuacao=pontuacao, emissao=emissao)
    
@user_bp.route('/logout')
def logout_usuario():
    session.pop('user_role', None)
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('index'))


