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
    return render(request, 'consultas/registrar_atendimento.html', {
        'form': form,
        'atendimentos_hoje': atendimentos_hoje,
        'atendimentos_anteriores': atendimentos_anteriores,
    })
