# Generated by Django 5.0.7 on 2024-07-31 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liriodosvales', '0004_remove_atendimentomedico_hipotese_diagnostica_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='atendimentomedico',
            name='historia_doenca_atual',
            field=models.TextField(blank=True, null=True),
        ),
    ]
