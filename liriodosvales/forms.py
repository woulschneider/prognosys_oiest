from django import forms
from .models import Paciente
from django.forms.widgets import DateInput

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'cpf', 'data_nascimento', 'endereco', 'telefone', 'sexo']
        widgets = {
            'data_nascimento': DateInput(attrs={'type': 'text', 'placeholder': 'dd/mm/yyyy'}, format=('%d/%m/%Y')),
            'sexo': forms.Select(choices=[('Masculino', 'Masculino'), ('Feminino', 'Feminino')]),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_nascimento'].input_formats = ['%d/%m/%Y']