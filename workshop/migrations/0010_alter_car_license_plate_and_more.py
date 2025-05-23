# Generated by Django 5.2.1 on 2025-05-18 06:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0009_historicalservice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='license_plate',
            field=models.CharField(max_length=10, unique=True, validators=[django.core.validators.RegexValidator(message='Placa inválida. Use o padrão brasileiro (ex: ABC1D23 ou ABC-1234).', regex='^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$|^[A-Z]{3}-?[0-9]{4}$')], verbose_name='Placa'),
        ),
        migrations.AlterField(
            model_name='historicalservice',
            name='parts_cost',
            field=models.DecimalField(decimal_places=2, default=False, max_digits=10, verbose_name='Custo de Peças'),
        ),
        migrations.AlterField(
            model_name='historicalservice',
            name='total_cost',
            field=models.DecimalField(decimal_places=2, default=False, editable=False, max_digits=10, verbose_name='Custo Total'),
        ),
        migrations.AlterField(
            model_name='service',
            name='parts_cost',
            field=models.DecimalField(decimal_places=2, default=False, max_digits=10, verbose_name='Custo de Peças'),
        ),
        migrations.AlterField(
            model_name='service',
            name='total_cost',
            field=models.DecimalField(decimal_places=2, default=False, editable=False, max_digits=10, verbose_name='Custo Total'),
        ),
    ]
