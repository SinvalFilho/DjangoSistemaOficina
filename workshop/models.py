from datetime import date, timezone
from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from django.forms import ValidationError
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords 
import uuid

# Validadores
cpf_cnpj_validator = RegexValidator(
    regex=r"^(?:\d{11}|\d{14})$",
    message=_('CPF/CNPJ inválido')
)

phone_validator = RegexValidator(
    regex=r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$',
    message=_('Telefone inválido')
)

plate_validator = RegexValidator(
    regex=r'^[A-Z]{3}-?[0-9]{4}$|^[A-Z]{3}[0-9][A-Z][0-9]{2}$',
    message=_('Placa inválida')
)

def generate_token():
    return uuid.uuid4().hex[:6].upper()

class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_("Nome"))

    class Meta:
        ordering = ['name']
        verbose_name = _('Marca')
        verbose_name_plural = _('Marcas')

    def save(self, *args, **kwargs):
        self.name = capfirst(self.name.strip())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class CarModel(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='models', verbose_name=_("Marca"))
    name = models.CharField(max_length=50, verbose_name=_("Nome do modelo"))

    class Meta:
        unique_together = ('brand', 'name')
        ordering = ['brand__name', 'name']
        verbose_name = _('Modelo de Carro')
        verbose_name_plural = _('Modelos de Carros')

    def save(self, *args, **kwargs):
        self.name = capfirst(self.name.strip())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand} {self.name}"

class Generation(models.Model):
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name='generations', verbose_name=_("Modelo"))
    number = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name=_("Número da geração"))

    class Meta:
        unique_together = ('car_model', 'number')
        ordering = ['car_model__brand__name', 'car_model__name', 'number']
        verbose_name = _('Geração')
        verbose_name_plural = _('Gerações')

    def clean(self):
        if self.number < 1:
            raise ValidationError({'number': _('Geração deve ser maior que zero')})

    def __str__(self):
        return f"Geração {self.number}"

class CarCategory(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_("Categoria"))

    class Meta:
        ordering = ['name']
        verbose_name = _('Categoria de Carro')
        verbose_name_plural = _('Categorias de Carros')

    def save(self, *args, **kwargs):
        self.name = capfirst(self.name.strip())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Nome"))
    cpf_cnpj = models.CharField(max_length=14, blank=True, null=True, validators=[cpf_cnpj_validator], verbose_name=_("CPF/CNPJ"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Criado em"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Atualizado em"))

    class Meta:
        ordering = ['name']
        verbose_name = _('Cliente')
        verbose_name_plural = _('Clientes')

    def save(self, *args, **kwargs):
        self.name = self.name.strip()
        if self.cpf_cnpj:
            self.cpf_cnpj = self.cpf_cnpj.strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class PhoneNumber(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='phones', verbose_name=_("Cliente"))
    number = models.CharField(max_length=20, validators=[phone_validator], verbose_name=_("Número de telefone"))
    is_whatsapp = models.BooleanField(default=False, verbose_name=_("É WhatsApp?"))

    class Meta:
        verbose_name = _('Telefone')
        verbose_name_plural = _('Telefones')

    def save(self, *args, **kwargs):
        self.number = self.number.strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.number}{' (WhatsApp)' if self.is_whatsapp else ''}"

class EmailAddress(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='emails', verbose_name=_("Cliente"))
    email = models.EmailField(verbose_name=_("E-mail"))

    class Meta:
        verbose_name = _('E-mail')
        verbose_name_plural = _('E-mails')

    def save(self, *args, **kwargs):
        self.email = self.email.strip().lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

class Car(models.Model):
    class FuelType(models.TextChoices):
        FLEX = 'flex', _('Flex')
        ALCOOL = 'alcohol', _('Álcool')
        GASOLINA = 'gasoline', _('Gasolina')
        DIESEL = 'diesel', _('Diesel')
        HIBRIDO = 'hybrid', _('Híbrido')

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='cars', verbose_name=_("Cliente"))
    license_plate = models.CharField(max_length=10, unique=True, validators=[plate_validator], verbose_name=_("Placa"))
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, verbose_name=_("Marca"))
    model = models.ForeignKey(CarModel, on_delete=models.PROTECT, verbose_name=_("Modelo"))
    generation = models.ForeignKey(Generation, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Geração"))
    year = models.PositiveIntegerField(validators=[MinValueValidator(1886)], verbose_name=_("Ano"))
    category = models.ForeignKey(CarCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Categoria"))
    fuel_type = models.CharField(max_length=20, choices=FuelType.choices, blank=True, null=True, verbose_name=_("Combustível"))

    class Meta:
        ordering = ['client', 'license_plate']
        verbose_name = _('Carro')
        verbose_name_plural = _('Carros')

    def save(self, *args, **kwargs):
        self.license_plate = self.license_plate.strip().upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.license_plate} - {self.brand} {self.model}"

class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Nome"))

    class Meta:
        ordering = ['name']
        verbose_name = _('Categoria de Serviço')
        verbose_name_plural = _('Categorias de Serviços')

    def save(self, *args, **kwargs):
        self.name = ' '.join(word.capitalize() for word in self.name.strip().split())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Service(models.Model):
    class ServiceType(models.TextChoices):
        DIAGNOSTICO = 'diagnosis', _('Diagnóstico')
        MANUTENCAO = 'maintenance', _('Manutenção')
        REPARO = 'repair', _('Reparo')
        OUTRO = 'other', _('Outro')

    class Status(models.TextChoices):
        RECEIVED = 'received', _('Recebido')
        BUDGETED = 'budgeted', _('Orçado')
        IN_PROGRESS = 'in_progress', _('Em Andamento')
        READY = 'ready', _('Pronto')
        DELIVERED = 'delivered', _('Entregue')

    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='services', verbose_name=_("Carro"))
    category = models.ManyToManyField(ServiceCategory, verbose_name=_("Categorias"))
    technician = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Técnico"))

    service_type = models.CharField(max_length=20, choices=ServiceType.choices, default=ServiceType.DIAGNOSTICO, verbose_name=_("Tipo de serviço"))
    description = models.TextField(blank=True, verbose_name=_("Descrição"))
    current_km = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Quilometragem atual"))

    labor_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_("Custo de mão de obra"))
    parts_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_("Custo de peças"))
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, editable=False, verbose_name=_("Custo total"))
    is_budgeted = models.BooleanField(default=False, verbose_name=_("Orçamento confirmado"))

    entry_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Data de entrada"))
    deadline_date = models.DateField(null=True, blank=True, verbose_name=_("Prazo"))
    start_date = models.DateTimeField(null=True, blank=True, verbose_name=_("Início"))
    completion_date = models.DateTimeField(null=True, blank=True, verbose_name=_("Conclusão"))
    delivery_date = models.DateTimeField(null=True, blank=True, verbose_name=_("Entrega"))

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.RECEIVED, verbose_name=_("Status"))
    whatsapp_notified = models.BooleanField(default=False, verbose_name=_("Notificado por WhatsApp"))
    email_notified = models.BooleanField(default=False, verbose_name=_("Notificado por e-mail"))

    receipt_image = models.ImageField(upload_to='receipts/', null=True, blank=True, verbose_name=_("Imagem da nota fiscal"))
    history = HistoricalRecords()

    class Meta:
        ordering = ['-entry_date']
        verbose_name = _('Serviço')
        verbose_name_plural = _('Serviços')

    def clean(self):
        if self.deadline_date and self.deadline_date < date.today():
            raise ValidationError({'deadline_date': _('Data de prazo deve ser futura')})
        if self.status in [self.Status.IN_PROGRESS, self.Status.READY, self.Status.DELIVERED]:
            if not self.is_budgeted:
                raise ValidationError({'is_budgeted': _('Orçamento deve ser confirmado')})
            if None in [self.labor_cost, self.parts_cost]:
                raise ValidationError(_('Informe todos os custos'))

    def save(self, *args, **kwargs):
        self.update_total_cost()
        self.update_status_dates()
        super().save(*args, **kwargs)

    def update_total_cost(self):
        if None not in [self.labor_cost, self.parts_cost]:
            self.total_cost = self.labor_cost + self.parts_cost

    def update_status_dates(self):
        if not self.pk:
            return
        now = timezone.now()
        original = Service.objects.get(pk=self.pk)
        if original.status != self.status:
            if self.status == self.Status.IN_PROGRESS and not self.start_date:
                self.start_date = now
            elif self.status == self.Status.READY and not self.completion_date:
                self.completion_date = now
            elif self.status == self.Status.DELIVERED and not self.delivery_date:
                self.delivery_date = now

    @property
    def total_paid(self):
        return sum(p.amount for p in self.payments.all()) if hasattr(self, 'payments') else 0

    @property
    def pending_amount(self):
        return max((self.total_cost or 0) - (self.total_paid or 0), 0)

    @property
    def service_duration(self):
        if self.start_date and self.completion_date:
            return self.completion_date - self.start_date

    @property
    def total_duration(self):
        if self.entry_date and self.delivery_date:
            return self.delivery_date - self.entry_date

    def __str__(self):
        return f"{self.get_service_type_display()} - {self.car.license_plate}"

class CarAccessToken(models.Model):
    car = models.OneToOneField(Car, on_delete=models.CASCADE, related_name='access_token', verbose_name=_("Carro"))
    token = models.CharField(max_length=10, unique=True, default=generate_token, verbose_name=_("Token"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Criado em"))
    expires_at = models.DateTimeField(verbose_name=_("Expira em"))

    class Meta:
        verbose_name = _('Token de Acesso')
        verbose_name_plural = _('Tokens de Acesso')

    def __str__(self):
        return f"{self.car.license_plate} - {self.token}"

class Payment(models.Model):
    class Method(models.TextChoices):
        CASH = 'cash', _('Dinheiro')
        DEBIT = 'debit', _('Débito')
        CREDIT = 'credit', _('Crédito')
        PIX = 'pix', _('Pix')

    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='payments', verbose_name=_("Serviço"))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Valor"))
    method = models.CharField(max_length=10, choices=Method.choices, verbose_name=_("Forma de pagamento"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Data"))

    class Meta:
        verbose_name = _('Pagamento')
        verbose_name_plural = _('Pagamentos')

    def __str__(self):
        return f"{self.get_method_display()} - R${self.amount}"
