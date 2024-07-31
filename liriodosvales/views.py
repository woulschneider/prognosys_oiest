from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .models import Paciente
from .forms import PacienteForm
from django.contrib import messages
from .models import Paciente, AtendimentoMedico
from .forms import AtendimentoMedicoForm
from django.template.loader import render_to_string

def home(request):
    return render(request, 'liriodosvales/home.html') 

def listar_pacientes(request):
    pacientes = Paciente.objects.all().order_by('nome')
    return render(request, 'liriodosvales/listar_pacientes.html', {'pacientes': pacientes}) 

from django.shortcuts import render, redirect, get_object_or_404
from .forms import PacienteForm
from .models import Paciente, Medicacao, Alergia, Diagnostico

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
    medicacoes = [(med.nome, med.dosagem, med.posologia) for med in paciente.medicacoes.all()]
    alergias = [alergia.nome for alergia in paciente.alergias.all()]
    diagnosticos = [(diag.nome, diag.codigo_cid) for diag in paciente.diagnosticos.all()]

    return render(request, 'liriodosvales/editar_paciente.html', {
        'form': form,
        'medicacoes': medicacoes,
        'alergias': alergias,
        'diagnosticos': diagnosticos
    })

def remover_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    paciente.delete()
    return redirect('liriodosvales:listar_pacientes')

def detalhes_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    medicacoes = paciente.medicacoes.all()
    alergias = paciente.alergias.all()
    diagnosticos = paciente.diagnosticos.all()

    return render(request, 'liriodosvales/detalhes_paciente.html', {
        'paciente': paciente,
        'medicacoes': medicacoes,
        'alergias': alergias,
        'diagnosticos': diagnosticos
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from .models import Paciente, AtendimentoMedico, Diagnostico
from .forms import AtendimentoMedicoForm
import json

def atendimento_medico(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    atendimentos_anteriores = paciente.atendimentos.order_by('-data_atendimento')
    is_primeiro_atendimento = not atendimentos_anteriores.exists()
    
    if request.method == 'POST':
        form = AtendimentoMedicoForm(request.POST, is_primeiro_atendimento=is_primeiro_atendimento)
        if form.is_valid():
            atendimento = form.save(commit=False)
            atendimento.paciente = paciente
            atendimento.save()
            return redirect(reverse('liriodosvales:imprimir_atendimento', kwargs={'atendimento_id': atendimento.id}))
    else:
        form = AtendimentoMedicoForm(is_primeiro_atendimento=is_primeiro_atendimento)
    
    tipo_atendimento = "Primeiro Atendimento" if is_primeiro_atendimento else "Reavaliação"
    medicacoes = paciente.medicacoes.all()
    
    diagnosticos = list(Diagnostico.objects.values('nome', 'codigo_cid'))
    
    context = {
        'paciente': paciente,
        'form': form,
        'medicacoes': medicacoes,
        'tipo_atendimento': tipo_atendimento,
        'atendimentos_anteriores': atendimentos_anteriores,
        'is_primeiro_atendimento': is_primeiro_atendimento,
        'diagnosticos_json': json.dumps(diagnosticos),
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

from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from .models import AtendimentoMedico

def imprimir_atendimento(request, atendimento_id):
    atendimento = get_object_or_404(AtendimentoMedico, id=atendimento_id)
    html_string = render_to_string('liriodosvales/imprimir_atendimento.html', {'atendimento': atendimento})
    
    response = HttpResponse(html_string)
    response['Content-Type'] = 'text/html'
    response['Content-Disposition'] = 'inline; filename="atendimento.html"'
    
    return response