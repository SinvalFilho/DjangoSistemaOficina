from itertools import count
from django.contrib import admin
from django.utils.html import format_html
from django.utils.timezone import now
from django.db.models import Sum, Count
from .models import (
    Brand, CarModel, Generation, CarCategory,
    Client, PhoneNumber, EmailAddress, Car,
    ServiceCategory, Service, Payment
)
from datetime import date, timezone

# ========== INLINES ==========

class PhoneNumberInline(admin.TabularInline):
    model = PhoneNumber
    extra = 1

class EmailAddressInline(admin.TabularInline):
    model = EmailAddress
    extra = 1

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('method', 'amount', 'created_at')

# ========== CLIENTES ==========

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    search_fields = ('name', 'cpf_cnpj')
    list_display = ('name', 'cpf_cnpj', 'get_phones', 'get_emails')
    inlines = [PhoneNumberInline, EmailAddressInline]

    def get_phones(self, obj):
        return ', '.join([
            f"{p.number}{' (WhatsApp)' if p.is_whatsapp else ''}"
            for p in obj.phones.all()
        ])
    get_phones.short_description = 'Telefones'

    def get_emails(self, obj):
        return ', '.join([e.email for e in obj.emails.all()])
    get_emails.short_description = 'E-mails'

# ========== CARROS ==========

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = (
        'license_plate', 'get_client', 'brand', 'model',
        'generation', 'year', 'fuel_type', 'get_service_count'
    )
    search_fields = ('license_plate', 'client__name', 'model__name')
    list_filter = ('brand', 'model', 'generation', 'fuel_type')
    autocomplete_fields = ('client', 'brand', 'model', 'generation', 'category')

    def get_client(self, obj):
        return obj.client.name
    get_client.short_description = 'Cliente'

    def get_service_count(self, obj):
        return f"{obj.services.count()} serviços"
    get_service_count.short_description = 'Qtd. de Serviços'

    Car._meta.verbose_name = "Carro"
    Car._meta.verbose_name_plural = "Carros"

# ========== SERVIÇOS ==========

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'get_client_name', 'get_license_plate', 'get_model_name',
        'entry_date', 'status', 'total_cost', 'total_paid', 'pending_amount'
    )
    search_fields = ('car__client__name', 'car__license_plate', 'car__model__name')
    list_filter = ('status', ('entry_date', admin.DateFieldListFilter), 'car__client')
    autocomplete_fields = ['car']
    filter_horizontal = ('category',)
    inlines = [PaymentInline]
    change_list_template = 'admin/services_change_list.html'

    readonly_fields = (
        'entry_date', 'total_cost', 'total_paid', 'pending_amount', 
        'receipt_preview', 'service_duration', 'total_duration'
    )

    fieldsets = (
        ('Informações do Carro', {
            'fields': ('car', 'current_km')
        }),
        ('Detalhes do Serviço', {
            'fields': (
                'service_type', 'category', 'description', 'status',
                ('entry_date', 'start_date', 'completion_date', 'delivery_date'),
                'deadline_date', 'technician'
            )
        }),
        ('Custos', {
            'fields': (
                ('labor_cost', 'parts_cost', 'total_cost'),
                ('total_paid', 'pending_amount'),
                'is_budgeted'
            )
        }),
        ('Notificações', {
            'fields': ('whatsapp_notified', 'email_notified'),
            'classes': ('collapse',)
        }),
        ('Documentação', {
            'fields': ('receipt_image', 'receipt_preview'),
            'classes': ('collapse',)
        }),
        ('Tempos', {
            'fields': ('service_duration', 'total_duration'),
            'classes': ('collapse',)
        }),
    )

    # Métodos auxiliares para exibição na lista
    def get_client_name(self, obj):
        return obj.car.client.name
    get_client_name.short_description = 'Cliente'
    get_client_name.admin_order_field = 'car__client__name'

    def get_license_plate(self, obj):
        return obj.car.license_plate
    get_license_plate.short_description = 'Placa'
    get_license_plate.admin_order_field = 'car__license_plate'

    def get_model_name(self, obj):
        return f"{obj.car.brand} {obj.car.model}"
    get_model_name.short_description = 'Modelo'
    get_model_name.admin_order_field = 'car__model__name'

    def receipt_preview(self, obj):
        if obj.receipt_image:
            return format_html(
                '<img src="{}" width="300" style="max-height:200px;" />',
                obj.receipt_image.url
            )
        return "Sem imagem"
    receipt_preview.short_description = "Visualização do Recibo"

    def service_duration(self, obj):
        if obj.start_date and obj.completion_date:
            duration = obj.completion_date - obj.start_date
            days = duration.days
            hours, remainder = divmod(duration.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            return f"{days}d {hours}h {minutes}m"
        return "-"
    service_duration.short_description = "Duração do Serviço"

    def total_duration(self, obj):
        if obj.entry_date and obj.delivery_date:
            duration = obj.delivery_date - obj.entry_date
            days = duration.days
            hours, remainder = divmod(duration.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            return f"{days}d {hours}h {minutes}m"
        return "-"
    total_duration.short_description = "Tempo Total"

    def save_model(self, request, obj, form, change):
        # Atualiza automaticamente as datas baseadas no status
        if not change:  # Novo registro
            obj.entry_date = timezone.now()
        
        if 'status' in form.changed_data:
            now = timezone.now()
            if obj.status == Service.Status.IN_PROGRESS and not obj.start_date:
                obj.start_date = now
            elif obj.status == Service.Status.READY and not obj.completion_date:
                obj.completion_date = now
            elif obj.status == Service.Status.DELIVERED and not obj.delivery_date:
                obj.delivery_date = now
        
        super().save_model(request, obj, form, change)

    def changelist_view(self, request, extra_context=None):
        today = date.today()
        qs = self.get_queryset(request)
        
        def get_stats(qs_filter):
            filtered_qs = qs.filter(**qs_filter)
            labor = filtered_qs.aggregate(Sum('labor_cost'))['labor_cost__sum'] or 0
            parts = filtered_qs.aggregate(Sum('parts_cost'))['parts_cost__sum'] or 0
            total_cost = labor + parts
            total_paid = filtered_qs.aggregate(paid=Sum('payments__amount'))['paid'] or 0
            return {
                'count': filtered_qs.count(),
                'total_cost': total_cost,
                'total_paid': total_paid,
                'pending': total_cost - total_paid
            }

        stats = {
            'today': get_stats({'entry_date__date': today}),
            'month': get_stats({'entry_date__month': today.month, 'entry_date__year': today.year}),
            'year': get_stats({'entry_date__year': today.year}),
            'all_time': get_stats({}),
        }

        extra_context = extra_context or {}
        extra_context.update({
            'stats': stats,
            'status_counts': dict(qs.values_list('status').annotate(count=Count('id')))
        })

        return super().changelist_view(request, extra_context=extra_context)

# ========== OUTROS MODELOS ==========

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('brand', 'name')
    list_filter = ('brand',)
    search_fields = ('name',)

@admin.register(Generation)
class GenerationAdmin(admin.ModelAdmin):
    list_display = ('car_model', 'number')
    list_filter = ('car_model__brand',)
    search_fields = ('car_model__name',)

@admin.register(CarCategory)
class CarCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
