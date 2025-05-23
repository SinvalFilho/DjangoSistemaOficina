# Generated by Django 5.2.1 on 2025-05-19 02:40

import django.core.validators
import django.db.models.deletion
import workshop.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0015_alter_car_options_alter_caraccesstoken_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='car',
            options={'ordering': ['client', 'license_plate'], 'verbose_name': 'Carro', 'verbose_name_plural': 'Carros'},
        ),
        migrations.AlterModelOptions(
            name='caraccesstoken',
            options={'verbose_name': 'Token de Acesso', 'verbose_name_plural': 'Tokens de Acesso'},
        ),
        migrations.AlterModelOptions(
            name='carcategory',
            options={'ordering': ['name'], 'verbose_name': 'Categoria de Carro', 'verbose_name_plural': 'Categorias de Carros'},
        ),
        migrations.AlterModelOptions(
            name='carmodel',
            options={'ordering': ['brand__name', 'name'], 'verbose_name': 'Modelo de Carro', 'verbose_name_plural': 'Modelos de Carros'},
        ),
        migrations.AlterModelOptions(
            name='client',
            options={'ordering': ['name'], 'verbose_name': 'Cliente', 'verbose_name_plural': 'Clientes'},
        ),
        migrations.AlterModelOptions(
            name='emailaddress',
            options={'verbose_name': 'E-mail', 'verbose_name_plural': 'E-mails'},
        ),
        migrations.AlterModelOptions(
            name='generation',
            options={'ordering': ['car_model__brand__name', 'car_model__name', 'number'], 'verbose_name': 'Geração', 'verbose_name_plural': 'Gerações'},
        ),
        migrations.AlterModelOptions(
            name='historicalservice',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Serviço', 'verbose_name_plural': 'historical Serviços'},
        ),
        migrations.AlterModelOptions(
            name='payment',
            options={'verbose_name': 'Pagamento', 'verbose_name_plural': 'Pagamentos'},
        ),
        migrations.AlterModelOptions(
            name='phonenumber',
            options={'verbose_name': 'Telefone', 'verbose_name_plural': 'Telefones'},
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'ordering': ['-entry_date'], 'verbose_name': 'Serviço', 'verbose_name_plural': 'Serviços'},
        ),
        migrations.AlterModelOptions(
            name='servicecategory',
            options={'ordering': ['name'], 'verbose_name': 'Categoria de Serviço', 'verbose_name_plural': 'Categorias de Serviços'},
        ),
        migrations.AlterField(
            model_name='brand',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='car',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='workshop.brand', verbose_name='Marca'),
        ),
        migrations.AlterField(
            model_name='car',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='workshop.carcategory', verbose_name='Categoria'),
        ),
        migrations.AlterField(
            model_name='car',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cars', to='workshop.client', verbose_name='Cliente'),
        ),
        migrations.AlterField(
            model_name='car',
            name='fuel_type',
            field=models.CharField(blank=True, choices=[('flex', 'Flex'), ('alcohol', 'Álcool'), ('gasoline', 'Gasolina'), ('diesel', 'Diesel'), ('hybrid', 'Híbrido')], max_length=20, null=True, verbose_name='Combustível'),
        ),
        migrations.AlterField(
            model_name='car',
            name='generation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='workshop.generation', verbose_name='Geração'),
        ),
        migrations.AlterField(
            model_name='car',
            name='license_plate',
            field=models.CharField(max_length=10, unique=True, validators=[django.core.validators.RegexValidator(message='Placa inválida', regex='^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$|^[A-Z]{3}-?[0-9]{4}$')], verbose_name='Placa'),
        ),
        migrations.AlterField(
            model_name='car',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='workshop.carmodel', verbose_name='Modelo'),
        ),
        migrations.AlterField(
            model_name='car',
            name='year',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1886)], verbose_name='Ano'),
        ),
        migrations.AlterField(
            model_name='caraccesstoken',
            name='car',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='access_token', to='workshop.car', verbose_name='Carro'),
        ),
        migrations.AlterField(
            model_name='caraccesstoken',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Criado em'),
        ),
        migrations.AlterField(
            model_name='caraccesstoken',
            name='expires_at',
            field=models.DateTimeField(verbose_name='Expira em'),
        ),
        migrations.AlterField(
            model_name='caraccesstoken',
            name='token',
            field=models.CharField(default=workshop.models.generate_token, max_length=10, unique=True, verbose_name='Token'),
        ),
        migrations.AlterField(
            model_name='carcategory',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Categoria'),
        ),
        migrations.AlterField(
            model_name='carmodel',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='models', to='workshop.brand', verbose_name='Marca'),
        ),
        migrations.AlterField(
            model_name='carmodel',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Nome do modelo'),
        ),
        migrations.AlterField(
            model_name='client',
            name='cpf_cnpj',
            field=models.CharField(blank=True, max_length=14, null=True, validators=[django.core.validators.RegexValidator(message='CPF/CNPJ inválido', regex='^(?:\\d{11}|\\d{14})$')], verbose_name='CPF/CNPJ'),
        ),
        migrations.AlterField(
            model_name='client',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Criado em'),
        ),
        migrations.AlterField(
            model_name='client',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='client',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Atualizado em'),
        ),
        migrations.AlterField(
            model_name='emailaddress',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emails', to='workshop.client', verbose_name='Cliente'),
        ),
        migrations.AlterField(
            model_name='emailaddress',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='E-mail'),
        ),
        migrations.AlterField(
            model_name='generation',
            name='car_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='generations', to='workshop.carmodel', verbose_name='Modelo'),
        ),
        migrations.AlterField(
            model_name='generation',
            name='number',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Número da geração'),
        ),
        migrations.AlterField(
            model_name='historicalservice',
            name='car',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='workshop.car', verbose_name='Carro'),
        ),
        migrations.AlterField(
            model_name='historicalservice',
            name='completion_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Conclusão'),
        ),
        migrations.AlterField(
            model_name='historicalservice',
            name='current_km',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Quilometragem atual'),
        ),
        migrations.AlterField(
            model_name='historicalservice',
            name='deadline_date',
            field=models.DateField(blank=True, null=True, verbose_name='Prazo'),
        ),
        migrations.AlterField(
            model_name='historicalservice',
            name='delivery_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Entrega'),
        ),
        migrations.AlterField(
            model_name='historicalservice',
            name='description',
            field=models.TextField(blank=True, verbose_name='Descrição'),
        ),
        migrations.AlterField(
            model_name='historicalservice',
            name='email_notified',
            field=models.BooleanField(default=False, verbose_name='Notificado por e-mail'),
        ),
        migrations.AlterField(
            model_name='historicalservice',
            name='entry_date',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='Data de entrada'),
        ),
        migrations.AlterField(
            model_name='historicalservice',
            name='is_budgeted',
            field=models.BooleanField(default=False, verbose_name='Orçamento confirmado'),
        ),
        migrations.AlterField(
            model_name='historicalservice',
            name='labor_cost',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Custo de mão de obra'),
        ),
        migrations.AlterField(
            model_name='historicalservice',
            name='parts_cost',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Custo de peças'),
        ),
        migrations.AlterField(
            model_name='historicalservice',
            name='receipt_image',
            field=models.TextField(blank=True, max_length=100, null=True, verbose_name='Imagem da nota fiscal'),
        ),
        migrations.AlterField(
            model_name='historicalservice',
            name='service_type',
            field=models.CharField(choices=[('diagnosis', 'Diagnóstico'), ('maintenance', 'Manutenção'), ('repair', 'Reparo'), ('other', 'Outro')], default='diagnosis', max_length=20, verbose_name='Tipo de serviço'),
        ),
        migrations.AlterField(
            model_name='historicalservice',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Início'),
        ),
        migrations.AlterField(
            model_name='historicalservice',
            name='status',
            field=models.CharField(choices=[('received', 'Recebido'), ('budgeted', 'Orçado'), ('in_progress', 'Em Andamento'), ('ready', 'Pronto'), ('delivered', 'Entregue')], default='received', max_length=20, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='historicalservice',
            name='technician',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Técnico'),
        ),
        migrations.AlterField(
            model_name='historicalservice',
            name='total_cost',
            field=models.DecimalField(blank=True, decimal_places=2, editable=False, max_digits=10, null=True, verbose_name='Custo total'),
        ),
        migrations.AlterField(
            model_name='historicalservice',
            name='whatsapp_notified',
            field=models.BooleanField(default=False, verbose_name='Notificado por WhatsApp'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Data'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='method',
            field=models.CharField(choices=[('cash', 'Dinheiro'), ('debit', 'Débito'), ('credit', 'Crédito'), ('pix', 'Pix')], max_length=10, verbose_name='Forma de pagamento'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='workshop.service', verbose_name='Serviço'),
        ),
        migrations.AlterField(
            model_name='phonenumber',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phones', to='workshop.client', verbose_name='Cliente'),
        ),
        migrations.AlterField(
            model_name='phonenumber',
            name='is_whatsapp',
            field=models.BooleanField(default=False, verbose_name='É WhatsApp?'),
        ),
        migrations.AlterField(
            model_name='phonenumber',
            name='number',
            field=models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message='Telefone inválido', regex='^\\(?\\d{2}\\)?\\s?\\d{4,5}-?\\d{4}$')], verbose_name='Número de telefone'),
        ),
        migrations.AlterField(
            model_name='service',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='workshop.car', verbose_name='Carro'),
        ),
        migrations.AlterField(
            model_name='service',
            name='category',
            field=models.ManyToManyField(to='workshop.servicecategory', verbose_name='Categorias'),
        ),
        migrations.AlterField(
            model_name='service',
            name='completion_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Conclusão'),
        ),
        migrations.AlterField(
            model_name='service',
            name='current_km',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Quilometragem atual'),
        ),
        migrations.AlterField(
            model_name='service',
            name='deadline_date',
            field=models.DateField(blank=True, null=True, verbose_name='Prazo'),
        ),
        migrations.AlterField(
            model_name='service',
            name='delivery_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Entrega'),
        ),
        migrations.AlterField(
            model_name='service',
            name='description',
            field=models.TextField(blank=True, verbose_name='Descrição'),
        ),
        migrations.AlterField(
            model_name='service',
            name='email_notified',
            field=models.BooleanField(default=False, verbose_name='Notificado por e-mail'),
        ),
        migrations.AlterField(
            model_name='service',
            name='entry_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Data de entrada'),
        ),
        migrations.AlterField(
            model_name='service',
            name='is_budgeted',
            field=models.BooleanField(default=False, verbose_name='Orçamento confirmado'),
        ),
        migrations.AlterField(
            model_name='service',
            name='labor_cost',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Custo de mão de obra'),
        ),
        migrations.AlterField(
            model_name='service',
            name='parts_cost',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Custo de peças'),
        ),
        migrations.AlterField(
            model_name='service',
            name='receipt_image',
            field=models.ImageField(blank=True, null=True, upload_to='receipts/', verbose_name='Imagem da nota fiscal'),
        ),
        migrations.AlterField(
            model_name='service',
            name='service_type',
            field=models.CharField(choices=[('diagnosis', 'Diagnóstico'), ('maintenance', 'Manutenção'), ('repair', 'Reparo'), ('other', 'Outro')], default='diagnosis', max_length=20, verbose_name='Tipo de serviço'),
        ),
        migrations.AlterField(
            model_name='service',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Início'),
        ),
        migrations.AlterField(
            model_name='service',
            name='status',
            field=models.CharField(choices=[('received', 'Recebido'), ('budgeted', 'Orçado'), ('in_progress', 'Em Andamento'), ('ready', 'Pronto'), ('delivered', 'Entregue')], default='received', max_length=20, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='service',
            name='technician',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Técnico'),
        ),
        migrations.AlterField(
            model_name='service',
            name='total_cost',
            field=models.DecimalField(blank=True, decimal_places=2, editable=False, max_digits=10, null=True, verbose_name='Custo total'),
        ),
        migrations.AlterField(
            model_name='service',
            name='whatsapp_notified',
            field=models.BooleanField(default=False, verbose_name='Notificado por WhatsApp'),
        ),
        migrations.AlterField(
            model_name='servicecategory',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Nome'),
        ),
    ]
