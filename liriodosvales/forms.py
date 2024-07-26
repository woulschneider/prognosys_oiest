from django import forms
from .models import Paciente, Medicacao, Alergia, Diagnostico
from django.forms.widgets import DateInput

class PacienteForm(forms.ModelForm):
    nova_medicacao_nome = forms.CharField(required=False, label='Nova Medicação')
    nova_medicacao_dosagem = forms.CharField(required=False, label='Dosagem')
    nova_alergia_nome = forms.CharField(required=False, label='Nova Alergia')
    nova_alergia_tipo = forms.CharField(required=False, label='Tipo')
    novo_diagnostico_nome = forms.CharField(required=False, label='Novo Diagnóstico')
    novo_diagnostico_codigo_cid = forms.CharField(required=False, label='Código CID')

    class Meta:
        model = Paciente
        fields = ['nome', 'cpf', 'data_nascimento', 'endereco', 'telefone', 'sexo', 'medicacoes', 'alergias', 'diagnosticos']
        widgets = {
            'data_nascimento': DateInput(attrs={'type': 'date'}, format='%d/%m/%Y'),
            'sexo': forms.Select(choices=[('Masculino', 'Masculino'), ('Feminino', 'Feminino')]),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_nascimento'].input_formats = ['%d/%m/%Y']
