from django.urls import path
from . import views

app_name = 'consultas'

urlpatterns = [
    path('', views.registrar_atendimento, name='lista_atendimentos'),
    path('imprimir/', views.imprimir_atendimentos, name='imprimir_atendimentos'),
]
