# Generated by Django 5.2.1 on 2025-05-18 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0003_alter_brand_options_alter_car_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='total_cost',
            field=models.DecimalField(blank=True, decimal_places=2, editable=False, max_digits=10, verbose_name='Custo Total'),
        ),
    ]
