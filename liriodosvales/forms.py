from django import forms
from .models import Paciente
from django.forms.widgets import DateInput

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'cpf', 'data_nascimento', 'endereco', 'telefone', 'sexo']
        widgets = {
            'data_nascimento': DateInput(attrs={'type': 'text', 'placeholder': 'dd/mm/yyyy'}, format=('%d/%m/%Y')),
            'sexo': forms.Select(choices=Paciente.SEXO_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_nascimento'].input_formats = ['%d/%m/%Y']
        
        # Definir campos obrigatórios
        self.fields['nome'].required = True
        self.fields['cpf'].required = True
        self.fields['data_nascimento'].required = True
        
        # Definir campos opcionais
        self.fields['endereco'].required = False
        self.fields['telefone'].required = False
        
        # Definir valores padrão
        self.fields['sexo'].initial = 'Masculino'