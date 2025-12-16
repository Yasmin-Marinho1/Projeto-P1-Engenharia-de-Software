from flask import render_template, request, redirect, url_for, session, flash
from . import user_bp

@user_bp.route('/formulario', methods=['GET', 'POST'])
def formulario():
    '''
    lógica do formulário
    '''
    return "formulario"

@user_bp.route('/logout')
def logout_usuario():
    '''
    logica logout_usuario
    '''
    return "logout"


