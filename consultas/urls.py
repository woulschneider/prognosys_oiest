from django.urls import path
from . import views

urlpatterns = [
    path('', views.registrar_atendimento, name='lista_atendimentos'),
]
