from django.urls import path
from . import views

app_name = 'liriodosvales'

urlpatterns = [
    path('', views.home, name='home'),
    path('listar_pacientes', views.listar_pacientes, name='listar_pacientes'),
    path('novo_paciente', views.novo_paciente, name='novo_paciente'),
    path('editar_paciente/<int:paciente_id>/', views.editar_paciente, name='editar_paciente'),
    path('remover_paciente/<int:paciente_id>/', views.remover_paciente, name='remover_paciente'),
    path('detalhes_paciente/<int:paciente_id>/', views.detalhes_paciente, name='detalhes_paciente'),
    
]
