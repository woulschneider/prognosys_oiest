from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Paciente, Medicacao, Alergia, Diagnostico, AtendimentoMedico, ExameComplementar, Encaminhamento
from .forms import PacienteForm, AtendimentoMedicoForm
from .utils import processar_conduta
import json
import re
from django.template.loader import render_to_string


def home(request):
    return render(request, 'liriodosvales/home.html')

def listar_pacientes(request):
    pacientes = Paciente.objects.all().order_by('nome')
    return render(request, 'liriodosvales/listar_pacientes.html', {'pacientes': pacientes})

def remover_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    if request.method == 'POST':
        paciente.delete()
        messages.success(request, f'Paciente {paciente.nome} removido com sucesso.')
        return redirect('liriodosvales:listar_pacientes')
    return render(request, 'liriodosvales/confirmar_remocao_paciente.html', {'paciente': paciente})

def detalhes_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    medicacoes = paciente.medicacoes.all()
    alergias = paciente.alergias.all()
    diagnosticos = paciente.diagnosticos.all()
    context = {
        'paciente': paciente,
        'medicacoes': medicacoes,
        'alergias': alergias,
        'diagnosticos': diagnosticos,
    }
    return render(request, 'liriodosvales/detalhes_paciente.html', context)

def novo_paciente(request):
    medicacoes = []
    alergias = []
    diagnosticos = []

    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save(commit=False)
            paciente.save()

            # Processar e salvar medicações
            medicacao_nomes = request.POST.getlist('medicacoes_nomes[]')
            medicacao_dosagens = request.POST.getlist('medicacoes_dosagens[]')
            medicacao_posologias = request.POST.getlist('medicacoes_posologias[]')
            for nome, dosagem, posologia in zip(medicacao_nomes, medicacao_dosagens, medicacao_posologias):
                if nome and dosagem and posologia:
                    medicacao = Medicacao(nome=nome, dosagem=dosagem, posologia=posologia)
                    medicacao.save()
                    paciente.medicacoes.add(medicacao)

            # Processar e salvar alergias
            alergia_nomes = request.POST.getlist('alergias_nomes[]')
            for nome in alergia_nomes:
                if nome:
                    alergia = Alergia(nome=nome)
                    alergia.save()
                    paciente.alergias.add(alergia)

            # Processar e salvar diagnósticos
            diagnostico_nomes = request.POST.getlist('diagnosticos_nomes[]')
            diagnostico_codigos_cid = request.POST.getlist('diagnosticos_codigos_cid[]')
            for nome, codigo_cid in zip(diagnostico_nomes, diagnostico_codigos_cid):
                if nome and codigo_cid:
                    diagnostico = Diagnostico(nome=nome, codigo_cid=codigo_cid)
                    diagnostico.save()
                    paciente.diagnosticos.add(diagnostico)

            messages.success(request, 'Paciente cadastrado com sucesso!')
            return redirect('liriodosvales:listar_pacientes')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Erro no campo {field}: {error}")
            # Preservar os dados inseridos nas listas
            medicacoes = zip(request.POST.getlist('medicacoes_nomes[]'), 
                             request.POST.getlist('medicacoes_dosagens[]'), 
                             request.POST.getlist('medicacoes_posologias[]'))
            alergias = request.POST.getlist('alergias_nomes[]')
            diagnosticos = zip(request.POST.getlist('diagnosticos_nomes[]'), 
                               request.POST.getlist('diagnosticos_codigos_cid[]'))
    else:
        form = PacienteForm()

    return render(request, 'liriodosvales/novo_paciente.html', {
        'form': form,
        'medicacoes': medicacoes,
        'alergias': alergias,
        'diagnosticos': diagnosticos
    })

def editar_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)

    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            paciente = form.save(commit=False)
            paciente.save()

            # Atualizar medicações
            paciente.medicacoes.clear()
            medicacao_nomes = request.POST.getlist('medicacoes_nomes[]')
            medicacao_dosagens = request.POST.getlist('medicacoes_dosagens[]')
            medicacao_posologias = request.POST.getlist('medicacoes_posologias[]')
            for nome, dosagem, posologia in zip(medicacao_nomes, medicacao_dosagens, medicacao_posologias):
                if nome and dosagem and posologia:
                    medicacao = Medicacao.objects.create(nome=nome, dosagem=dosagem, posologia=posologia)
                    paciente.medicacoes.add(medicacao)

            # Atualizar alergias
            paciente.alergias.clear()
            alergia_nomes = request.POST.getlist('alergias_nomes[]')
            for nome in alergia_nomes:
                if nome:
                    alergia = Alergia.objects.create(nome=nome)
                    paciente.alergias.add(alergia)

            # Atualizar diagnósticos
            paciente.diagnosticos.clear()
            diagnostico_nomes = request.POST.getlist('diagnosticos_nomes[]')
            diagnostico_codigos_cid = request.POST.getlist('diagnosticos_codigos_cid[]')
            for nome, codigo_cid in zip(diagnostico_nomes, diagnostico_codigos_cid):
                if nome and codigo_cid:
                    diagnostico = Diagnostico.objects.create(nome=nome, codigo_cid=codigo_cid)
                    paciente.diagnosticos.add(diagnostico)

            return redirect('liriodosvales:listar_pacientes')
    else:
        form = PacienteForm(instance=paciente)

    # Preparar dados para exibir no template
    medicacoes = [(m.nome, m.dosagem, m.posologia) for m in paciente.medicacoes.all()]
    alergias = [a.nome for a in paciente.alergias.all()]
    diagnosticos = [(d.nome, d.codigo_cid) for d in paciente.diagnosticos.all()]

    return render(request, 'liriodosvales/editar_paciente.html', {
        'form': form,
        'paciente': paciente,
        'medicacoes': medicacoes,
        'alergias': alergias,
        'diagnosticos': diagnosticos
    })

def atendimento_medico(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    atendimentos_anteriores = paciente.atendimentos.order_by('-data_atendimento')
    is_primeiro_atendimento = not atendimentos_anteriores.exists()
    ultimo_atendimento = atendimentos_anteriores.first() if atendimentos_anteriores.exists() else None
    
    if request.method == 'POST':
        form = AtendimentoMedicoForm(request.POST, is_primeiro_atendimento=is_primeiro_atendimento)
        if form.is_valid():
            atendimento = form.save(commit=False)
            atendimento.paciente = paciente
            
            hipotese_diagnostica_nome = form.cleaned_data.get('hipotese_diagnostica_nome', '')
            hipotese_diagnostica_cid = form.cleaned_data.get('hipotese_diagnostica_cid', '')
            
            if hipotese_diagnostica_nome and hipotese_diagnostica_cid:
                diagnostico, created = Diagnostico.objects.get_or_create(
                    nome=hipotese_diagnostica_nome,
                    codigo_cid=hipotese_diagnostica_cid
                )
                atendimento.hipotese_diagnostica = f"{diagnostico.nome} (CID: {diagnostico.codigo_cid})"
            
            atendimento.save()
            return redirect(reverse('liriodosvales:imprimir_atendimento', kwargs={'atendimento_id': atendimento.id}))
    else:
        form = AtendimentoMedicoForm(is_primeiro_atendimento=is_primeiro_atendimento)
    
    tipo_atendimento = "Primeiro Atendimento" if is_primeiro_atendimento else "Reavaliação"
    medicacoes = paciente.medicacoes.all()
    
    diagnosticos = list(Diagnostico.objects.values('nome', 'codigo_cid'))
    
    context = {
        'paciente': paciente,
        'paciente_id': paciente_id,  # Add this line
        'form': form,
        'medicacoes': medicacoes,
        'tipo_atendimento': tipo_atendimento,
        'atendimentos_anteriores': atendimentos_anteriores,
        'is_primeiro_atendimento': is_primeiro_atendimento,
        'diagnosticos_json': json.dumps(diagnosticos),
        'ultimo_atendimento': ultimo_atendimento,
    }
    
    return render(request, 'liriodosvales/atendimento_medico.html', context)

def buscar_cid(request):
    termo = request.GET.get('termo', '')
    diagnosticos = Diagnostico.objects.filter(nome__icontains=termo)[:10]
    resultados = [{'nome': d.nome, 'codigo_cid': d.codigo_cid} for d in diagnosticos]
    return JsonResponse(resultados, safe=False)

def atendimento_detalhes(request, atendimento_id):
    atendimento = get_object_or_404(AtendimentoMedico, id=atendimento_id)
    data = {
        'data': atendimento.data_atendimento.strftime('%d/%m/%Y %H:%M'),
        'tipo': atendimento.tipo_atendimento,
        'anamnese': atendimento.anamnese,
        'historia_patologica_pregressa': atendimento.historia_patologica_pregressa,
        'historia_familiar': atendimento.historia_familiar,
        'evolucao': atendimento.evolucao,
        'hipotese_diagnostica': atendimento.hipotese_diagnostica,
        'conduta': atendimento.conduta,
    }
    return JsonResponse(data)

def confirmacao_atendimento(request, atendimento_id):
    atendimento = get_object_or_404(AtendimentoMedico, id=atendimento_id)
    return render(request, 'liriodosvales/confirmacao_atendimento.html', {'atendimento': atendimento})

def imprimir_atendimento(request, atendimento_id):
    atendimento = get_object_or_404(AtendimentoMedico, id=atendimento_id)
    html_string = render_to_string('liriodosvales/imprimir_atendimento.html', {'atendimento': atendimento})
    
    response = HttpResponse(html_string)
    response['Content-Type'] = 'text/html'
    response['Content-Disposition'] = 'inline; filename="atendimento.html"'
    
    return response

def registrar_conduta(request, atendimento_id):
    atendimento = AtendimentoMedico.objects.get(id=atendimento_id)
    if request.method == 'POST':
        texto_conduta = request.POST.get('conduta')
        processar_conduta(texto_conduta, atendimento)
        return redirect('detalhes_atendimento', atendimento_id=atendimento.id)
    return render(request, 'template_atendimento.html', {'atendimento': atendimento})

@require_POST
@csrf_exempt
def aplicar_mudancas_medicacao(request):
    try:
        data = json.loads(request.body)
        paciente_id = data.get('paciente_id')
        atendimento_id = data.get('atendimento_id')
        mudancas = data.get('mudancas', [])

        paciente = get_object_or_404(Paciente, id=paciente_id)
        medicacoes_afetadas = []

        for mudanca in mudancas:
            partes = mudanca.split()
            if len(partes) < 3:
                continue

            acao = partes[0]
            nome = partes[1]
            dosagem = partes[2]
            posologia = ' '.join(partes[3:]) if len(partes) > 3 else ''

            if acao.startswith('+'):
                medicacao = Medicacao.objects.create(nome=nome, dosagem=dosagem, posologia=posologia)
                paciente.medicacoes.add(medicacao)
                medicacoes_afetadas.append(medicacao)
            elif acao.startswith('-'):
                medicacao = paciente.medicacoes.filter(nome=nome).first()
                if medicacao:
                    paciente.medicacoes.remove(medicacao)
                    medicacoes_afetadas.append(medicacao)

        response_data = {
            'success': True,
            'medicacoes': [{'nome': m.nome, 'dosagem': m.dosagem, 'posologia': m.posologia} for m in paciente.medicacoes.all()],
            'mensagens': [f"Medicação {m.nome} {'adicionada' if m in medicacoes_afetadas else 'removida'}" for m in medicacoes_afetadas]
        }
        return JsonResponse(response_data)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)