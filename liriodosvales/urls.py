from django.urls import path
from . import views

app_name = 'liriodosvales'

urlpatterns = [
    path('', views.home, name='home'),
    path('listar_pacientes.html', views.listar_pacientes, name='listar_pacientes'),
    path('novo_paciente.html', views.novo_paciente, name='novo_paciente')
    
]
