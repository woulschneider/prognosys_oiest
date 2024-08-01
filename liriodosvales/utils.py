import re
from .models import Medicacao, ExameComplementar, Encaminhamento

def processar_conduta(texto, atendimento):
    # Padrão para medicação: +nome dosagem posologia
    padrao_medicacao = r'\+(\w+)\s+(\d+\w+)\s+(.+)'
    
    # Padrão para exame: solicito nome_do_exame
    padrao_exame = r'solicito\s+(.+)'
    
    # Padrão para encaminhamento: encaminho à especialidade
    padrao_encaminhamento = r'encaminho\s+à\s+(.+)'

    for linha in texto.split('\n'):
        if match := re.match(padrao_medicacao, linha):
            nome, dosagem, posologia = match.groups()
            Medicacao.objects.create(
                nome=nome,
                dosagem=dosagem,
                posologia=posologia,
                atendimento=atendimento
            )
        elif match := re.match(padrao_exame, linha):
            nome_exame = match.group(1)
            ExameComplementar.objects.create(
                nome=nome_exame,
                atendimento=atendimento
            )
        elif match := re.match(padrao_encaminhamento, linha):
            especialidade = match.group(1)
            Encaminhamento.objects.create(
                especialidade=especialidade,
                atendimento=atendimento
            )