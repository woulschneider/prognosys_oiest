from django import forms
from .models import Atendimento

class AtendimentoForm(forms.ModelForm):
    class Meta:
        model = Atendimento
        fields = ['nome_paciente', 'tipo_atendimento', 'cid']
