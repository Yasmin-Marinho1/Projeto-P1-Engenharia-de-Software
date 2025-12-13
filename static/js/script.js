function alterarCampos() {
    // Ocultar campos dependendo do seu perfil de usuário
    const user_radio = document.getElementById('user');
    const empresa_radio = document.getElementById('empresa');
    const campo1 = document.getElementById('campo1');
    const campo2 = document.getElementById('campo2');
    if (user_radio.checked) {
        campo1.style.display = 'block';
        campo2.style.display = 'none';
    }
    else if (empresa_radio.checked) {
        campo2.style.display = 'block';
        campo1.style.display = 'none';
    }
    else {
        campo1.style.display ='none';
        campo2.style.display ='none';
    }
}
alterarCampos();
