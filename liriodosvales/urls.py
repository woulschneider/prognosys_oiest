from django.urls import path
from . import views

app_name = 'liriodosvales'

urlpatterns = [
    # ... outras URLs ...
    path('buscar-cid/', views.buscar_cid, name='buscar_cid'),
    # ... outras URLs ...
    path('confirmacao-atendimento/<int:atendimento_id>/', views.confirmacao_atendimento, name='confirmacao_atendimento'),
    path('imprimir-atendimento/<int:atendimento_id>/', views.imprimir_atendimento, name='imprimir_atendimento'),
    path('', views.home, name='home'),
    path('listar_pacientes', views.listar_pacientes, name='listar_pacientes'),
    path('novo_paciente', views.novo_paciente, name='novo_paciente'),
    path('editar_paciente/<int:paciente_id>/', views.editar_paciente, name='editar_paciente'),
    path('remover_paciente/<int:paciente_id>/', views.remover_paciente, name='remover_paciente'),
    path('detalhes_paciente/<int:paciente_id>/', views.detalhes_paciente, name='detalhes_paciente'),
    path('atendimento_medico/<int:paciente_id>/', views.atendimento_medico, name='atendimento_medico'),
    path('atendimento-detalhes/<int:atendimento_id>/', views.atendimento_detalhes, name='atendimento_detalhes'),
]