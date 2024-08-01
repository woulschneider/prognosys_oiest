# Generated by Django 5.0.7 on 2024-07-31 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liriodosvales', '0006_medicacao_atendimento_alter_medicacao_dosagem_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='atendimentomedico',
            name='anamnese',
        ),
        migrations.RemoveField(
            model_name='atendimentomedico',
            name='hipotese_diagnostica_cid',
        ),
        migrations.RemoveField(
            model_name='atendimentomedico',
            name='hipotese_diagnostica_nome',
        ),
        migrations.AddField(
            model_name='atendimentomedico',
            name='hipotese_diagnostica',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='atendimentomedico',
            name='conduta',
            field=models.TextField(blank=True, null=True),
        ),
    ]
