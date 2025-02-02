# Generated by Django 5.0.7 on 2024-07-30 23:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liriodosvales', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AtendimentoMedico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_atendimento', models.DateTimeField(auto_now_add=True)),
                ('tipo_atendimento', models.CharField(choices=[('PRIMEIRO', 'Primeiro Atendimento'), ('REAVALIACAO', 'Reavaliação')], max_length=20)),
                ('anamnese', models.TextField(blank=True, null=True)),
                ('historia_patologica_pregressa', models.TextField(blank=True, null=True)),
                ('historia_familiar', models.TextField(blank=True, null=True)),
                ('evolucao', models.TextField(blank=True, null=True)),
                ('hipotese_diagnostica', models.TextField()),
                ('conduta', models.TextField()),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='atendimentos', to='liriodosvales.paciente')),
            ],
        ),
    ]
