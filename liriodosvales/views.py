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

            return redirect('liriodosvales:editar_paciente', paciente_id=paciente.id)
        else:
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