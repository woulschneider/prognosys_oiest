# Generated by Django 5.0.7 on 2024-07-26 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Atendimento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_consulta', models.DateField(auto_now_add=True, verbose_name='Data da consulta')),
                ('nome_paciente', models.CharField(max_length=255, verbose_name='Nome do paciente')),
                ('tipo_atendimento', models.CharField(choices=[('PV', 'Primeira vez'), ('RT', 'Retorno')], default='PV', max_length=2, verbose_name='Tipo de atendimento')),
                ('cid', models.CharField(max_length=10, verbose_name='CID')),
            ],
            options={
                'db_table': 'consultas_atendimento',
            },
        ),
    ]
