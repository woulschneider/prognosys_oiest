from django.db import models

class Atendimento(models.Model):
    PRIMEIRA_VEZ = 'PV'
    RETORNO = 'RT'
    TIPO_ATENDIMENTO_CHOICES = [
        (PRIMEIRA_VEZ, 'Primeira vez'),
        (RETORNO, 'Retorno'),
    ]

    data_consulta = models.DateField(auto_now_add=True, verbose_name='Data da consulta')
    nome_paciente = models.CharField(max_length=255, verbose_name='Nome do paciente')
    tipo_atendimento = models.CharField(
        max_length=2,
        choices=TIPO_ATENDIMENTO_CHOICES,
        default=PRIMEIRA_VEZ,
        verbose_name='Tipo de atendimento'
    )
    cid = models.CharField(max_length=10, verbose_name='CID')

    def __str__(self):
        return f'{self.nome_paciente} - {self.data_consulta}'
