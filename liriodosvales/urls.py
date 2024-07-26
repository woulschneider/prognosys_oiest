from django.urls import path
from . import views

app_name = 'liriodosvales'

urlpatterns = [
    path('', views.home, name='home'),
    path('listar_pacientes', views.listar_pacientes, name='listar_pacientes'),
    path('novo_paciente', views.novo_paciente, name='novo_paciente')
    
]
