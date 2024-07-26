from django.shortcuts import render, redirect
from .models import Atendimento
from .forms import AtendimentoForm
from datetime import date

def registrar_atendimento(request):
    if request.method == 'POST':
        form = AtendimentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_atendimentos')
    else:
        form = AtendimentoForm()
    
    atendimentos_hoje = Atendimento.objects.filter(data_consulta=date.today())
    atendimentos_anteriores = Atendimento.objects.exclude(data_consulta=date.today())
    data_atual = date.today().strftime('%d/%m/%Y')
    
    return render(request, 'consultas/registrar_atendimento.html', {
        'form': form,
        'atendimentos_hoje': atendimentos_hoje,
        'atendimentos_anteriores': atendimentos_anteriores,
        'data_atual': data_atual,
    })

def imprimir_atendimentos(request):
    atendimentos_hoje = Atendimento.objects.filter(data_consulta=date.today())
    data_atual = date.today().strftime('%d/%m/%Y')
    
    return render(request, 'consultas/imprimir_atendimentos.html', {
        'atendimentos_hoje': atendimentos_hoje,
        'data_atual': data_atual,
    })