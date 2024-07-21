from django.shortcuts import redirect, render
from .models import Paciente
from .forms import PacienteForm

def home(request):
    return render(request, 'liriodosvales/home.html') 

def listar_pacientes(request):
    pacientes = Paciente.objects.all().order_by('nome')
    return render(request, 'liriodosvales/listar_pacientes.html', {'pacientes': pacientes}) 

def novo_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_pacientes')  # Redireciona para a lista de pacientes após o cadastro
    else:
        form = PacienteForm()
    return render(request, 'liriodosvales/novo_paciente.html', {'form': form})
