from django.shortcuts import redirect, render
from .models import Paciente
from .forms import PacienteForm

def home(request):
    return render(request, 'liriodosvales/home.html') 

def listar_pacientes(request):
    pacientes = Paciente.objects.all().order_by('nome')
    return render(request, 'liriodosvales/listar_pacientes.html', {'pacientes': pacientes}) 

from django.shortcuts import render, redirect, get_object_or_404
from .forms import PacienteForm
from .models import Paciente, Medicacao, Alergia, Diagnostico

def novo_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save(commit=False)
            paciente.save()
            # Adicionando nova medicação
            nova_medicacao_nome = form.cleaned_data.get('nova_medicacao_nome')
            nova_medicacao_dosagem = form.cleaned_data.get('nova_medicacao_dosagem')
            if nova_medicacao_nome and nova_medicacao_dosagem:
                medicacao = Medicacao(nome=nova_medicacao_nome, dosagem=nova_medicacao_dosagem)
                medicacao.save()
                paciente.medicacoes.add(medicacao)
            # Adicionando nova alergia
            nova_alergia_nome = form.cleaned_data.get('nova_alergia_nome')
            nova_alergia_tipo = form.cleaned_data.get('nova_alergia_tipo')
            if nova_alergia_nome:
                alergia = Alergia(nome=nova_alergia_nome, tipo=nova_alergia_tipo)
                alergia.save()
                paciente.alergias.add(alergia)
            # Adicionando novo diagnóstico
            novo_diagnostico_nome = form.cleaned_data.get('novo_diagnostico_nome')
            novo_diagnostico_codigo_cid = form.cleaned_data.get('novo_diagnostico_codigo_cid')
            if novo_diagnostico_nome:
                diagnostico = Diagnostico(nome=novo_diagnostico_nome, codigo_cid=novo_diagnostico_codigo_cid)
                diagnostico.save()
                paciente.diagnosticos.add(diagnostico)
            return redirect('liriodosvales:editar_paciente', paciente_id=paciente.id)
    else:
        form = PacienteForm()
    return render(request, 'liriodosvales/novo_paciente.html', {'form': form})

def editar_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            paciente = form.save(commit=False)
            paciente.save()
            # Adicionando nova medicação
            nova_medicacao_nome = form.cleaned_data.get('nova_medicacao_nome')
            nova_medicacao_dosagem = form.cleaned_data.get('nova_medicacao_dosagem')
            if nova_medicacao_nome and nova_medicacao_dosagem:
                medicacao = Medicacao(nome=nova_medicacao_nome, dosagem=nova_medicacao_dosagem)
                medicacao.save()
                paciente.medicacoes.add(medicacao)
            # Adicionando nova alergia
            nova_alergia_nome = form.cleaned_data.get('nova_alergia_nome')
            nova_alergia_tipo = form.cleaned_data.get('nova_alergia_tipo')
            if nova_alergia_nome:
                alergia = Alergia(nome=nova_alergia_nome, tipo=nova_alergia_tipo)
                alergia.save()
                paciente.alergias.add(alergia)
            # Adicionando novo diagnóstico
            novo_diagnostico_nome = form.cleaned_data.get('novo_diagnostico_nome')
            novo_diagnostico_codigo_cid = form.cleaned_data.get('novo_diagnostico_codigo_cid')
            if novo_diagnostico_nome:
                diagnostico = Diagnostico(nome=novo_diagnostico_nome, codigo_cid=novo_diagnostico_codigo_cid)
                diagnostico.save()
                paciente.diagnosticos.add(diagnostico)
    else:
        form = PacienteForm(instance=paciente)
    context = {
        'paciente': paciente,
        'form': form,
    }
    return render(request, 'liriodosvales/editar_paciente.html', context)

