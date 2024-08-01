from django import forms
from .models import AtendimentoMedico, Paciente
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

class AtendimentoMedicoForm(forms.ModelForm):
    class Meta:
        model = AtendimentoMedico
        fields = ['historia_doenca_atual', 'historia_patologica_pregressa', 'historia_familiar', 'evolucao', 'hipotese_diagnostica', 'conduta']

    def __init__(self, *args, is_primeiro_atendimento=True, **kwargs):
        super().__init__(*args, **kwargs)
        if not is_primeiro_atendimento:
            del self.fields['historia_doenca_atual']
            del self.fields['historia_patologica_pregressa']
            del self.fields['historia_familiar']