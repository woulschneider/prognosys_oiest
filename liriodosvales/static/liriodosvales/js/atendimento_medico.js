function atualizarListaMedicacoes(medicacoes) {
    const listaMedicacoes = document.getElementById('lista-medicacoes');
    if (!listaMedicacoes) {
        console.error('Element with id "lista-medicacoes" not found');
        return;
    }
    listaMedicacoes.innerHTML = '';
    medicacoes.forEach(med => {
        const li = document.createElement('li');
        li.className = 'list-group-item';
        li.textContent = `${med.nome} - ${med.dosagem} - ${med.posologia}`;
        listaMedicacoes.appendChild(li);
    });
    console.log('Lista de medicações atualizada:', medicacoes);
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function aplicarMudancasMedicacao() {
    const form = document.getElementById('atendimentoForm');
    const pacienteId = form.dataset.pacienteId;
    const atendimentoId = form.dataset.atendimentoId || null;

    const condutas = document.querySelectorAll('#condutas-list .list-group-item');
    const mudancas = Array.from(condutas)
        .map(conduta => conduta.querySelector('input[name="condutas_descricao[]"]').value)
        .filter(descricao => descricao.startsWith('+') || descricao.startsWith('++') || descricao.startsWith('--') || descricao.startsWith('-'));

    console.log('Mudanças a serem enviadas:', mudancas);

    if (mudancas.length > 0) {
        const requestBody = { 
            mudancas: mudancas, 
            paciente_id: pacienteId,
            atendimento_id: atendimentoId
        };
        console.log('Request body:', requestBody);

        fetch('/liriodosvales/aplicar-mudancas-medicacao/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(requestBody)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                console.log('Mudanças aplicadas com sucesso:', data);
                console.log('Medicações recebidas:', data.medicacoes);
                atualizarListaMedicacoes(data.medicacoes);
                exibirMensagensFlash(data.mensagens);
                // Clear the condutas list after successful application
                document.getElementById('condutas-list').innerHTML = '';
            } else {
                console.error('Erro ao aplicar mudanças:', data.error);
                alert('Erro ao aplicar mudanças: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Ocorreu um erro ao aplicar as mudanças. Por favor, tente novamente.');
        });
    } else {
        alert('Nenhuma mudança para aplicar.');
    }
}

function exibirMensagensFlash(mensagens) {
    const flashContainer = document.getElementById('flash-messages');
    flashContainer.innerHTML = '';
    mensagens.forEach(mensagem => {
        const flashMessage = document.createElement('div');
        flashMessage.className = 'alert alert-success alert-dismissible fade show';
        flashMessage.role = 'alert';
        flashMessage.innerHTML = `
            ${mensagem}
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
        `;
        flashContainer.appendChild(flashMessage);
    });
    
    // Auto-dismiss flash messages after 5 seconds
    setTimeout(() => {
        const alerts = flashContainer.querySelectorAll('.alert');
        alerts.forEach(alert => {
            $(alert).alert('close');
        });
    }, 5000);
}

function adicionarConduta() {
    const tipoConduta = document.getElementById('tipo_conduta').value;
    const descricaoConduta = document.getElementById('descricao_conduta').value;
    if (descricaoConduta.trim() === '') {
        alert('Por favor, insira uma descrição para a conduta.');
        return;
    }

    const condutasList = document.getElementById('condutas-list');
    const novaConduta = document.createElement('div');
    novaConduta.className = 'list-group-item d-flex justify-content-between align-items-center';
    novaConduta.innerHTML = `
        <span>${tipoConduta}: ${descricaoConduta}</span>
        <input type="hidden" name="condutas_descricao[]" value="${descricaoConduta}">
        <button type="button" class="btn btn-danger btn-sm" onclick="removerConduta(this)">
            <i class="fas fa-trash"></i>
        </button>
    `;
    condutasList.appendChild(novaConduta);

    document.getElementById('descricao_conduta').value = '';
}

function removerConduta(button) {
    button.closest('.list-group-item').remove();
}

// Make functions globally accessible
window.adicionarConduta = adicionarConduta;
window.removerConduta = removerConduta;
window.aplicarMudancasMedicacao = aplicarMudancasMedicacao;