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
    hipotese_diagnostica = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'hipotese_diagnostica_input'})
    )

    class Meta:
        model = AtendimentoMedico
        fields = ['anamnese', 'historia_doenca_atual', 'historia_patologica_pregressa', 'historia_familiar', 'evolucao', 'hipotese_diagnostica', 'conduta']

    def __init__(self, *args, is_primeiro_atendimento=True, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'hipotese_diagnostica':
                self.fields[field].widget.attrs.update({'class': 'form-control'})
        
        if not is_primeiro_atendimento:
            del self.fields['anamnese']
            del self.fields['historia_doenca_atual']
            del self.fields['historia_patologica_pregressa']
            del self.fields['historia_familiar']
        else:
            del self.fields['evolucao']

    def clean(self):
        cleaned_data = super().clean()
        hipotese_diagnostica = cleaned_data.get('hipotese_diagnostica', '')
        if '[' in hipotese_diagnostica and ']' in hipotese_diagnostica:
            nome, cid = hipotese_diagnostica.rsplit('[', 1)
            nome = nome.strip()
            cid = cid.rstrip(']').strip()
            cleaned_data['hipotese_diagnostica_nome'] = nome
            cleaned_data['hipotese_diagnostica_cid'] = cid
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.hipotese_diagnostica_nome = self.cleaned_data['hipotese_diagnostica_nome']
        instance.hipotese_diagnostica_cid = self.cleaned_data['hipotese_diagnostica_cid']
        if commit:
            instance.save()
        return instance