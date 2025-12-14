function alterarCampos() {
    // Ocultar campos dependendo do seu perfil de usuário
    const user_radio = document.getElementById('user');
    const empresa_radio = document.getElementById('empresa');
    const campo_usuario = document.getElementById('campo_usuario');
    const campo_empresa = document.getElementById('campo_empresa');
    const elementosEmpresa = campo_empresa.querySelectorAll('input');
    const elementosUsuario = campo_usuario.querySelectorAll('input');
    // Se a checkbox de usuários estiver marcada
    if (user_radio.checked) {
        // Exibe o campo de usuário comum e esconde o campo de empresas
        campo_usuario.style.display = 'block';
        campo_empresa.style.display = 'none';
        // Itera o campo de empresas e desabilita ele
        elementosEmpresa.forEach(elemento => {
            elemento.disabled = true
        });
        //Itera o campo de usuário comum e habilita ele
        elementosUsuario.forEach(elemento => {
            elemento.disabled = false
        });
    }

    // Se a checkbox de empresas estiver marcada
    else if (empresa_radio.checked) {
        // Exibe o campo de empresas e esconde o campo de usuário comum
        campo_empresa.style.display = 'block';
        campo_usuario.style.display = 'none';
        // Itera o campo de usuário comum e desabilita ele
        elementosUsuario.forEach(elemento => {
            elemento.disabled = true
        });
        //Itera o campo de empresa e habilita ele
        elementosEmpresa.forEach(elemento => {
            elemento.disabled = false
        });
    }
    else {
        campo_usuario.style.display ='none';
        campo_empresa.style.display ='none';
    }
    // Garante que o estado inicial seja configurado corretamente ao carregar a página
    document.addEventListener('DOMContentLoaded', (event) => {
        alterarCampos();
    });
}

// Função para validar pelo menos nome e sobrenome do usuário
function validarDoisNomes(form) {
    const inputNome = form.elements['nome'];
    const valorNome = inputNome.value.trim();
    
    // Divide a string por espaços e retira espaços duplos
    const nomes = valorNome.split(/\s+/);
    
    // Se não tiver dois nomes
    if (nomes.length < 2) {
        // Exibe mensagem pedindo nome completo
        inputNome.setCustomValidity('Por favor, insira pelo o seu nome completo.');
        // Não envia o formulário
        return false; 

    // Se tiver
    } else {
        // Limpa a mensagem pedindo nome completo(se tiver)
        inputNome.setCustomValidity(''); 
        // Envia o formulário
        return true;
    }
}
