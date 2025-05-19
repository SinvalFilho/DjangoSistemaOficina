from rest_framework import serializers
from .models import (
    Brand, CarModel, Generation, CarCategory,
    Client, PhoneNumber, EmailAddress, Car,
    ServiceCategory, Service, Payment
)

# ========== PHONE & EMAIL ==========
class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ['id', 'number', 'is_whatsapp']

class EmailAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailAddress
        fields = ['id', 'email']

# ========== CLIENT ==========
class ClientSerializer(serializers.ModelSerializer):
    phones = PhoneNumberSerializer(many=True, read_only=True)
    emails = EmailAddressSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'name', 'cpf_cnpj', 'phones', 'emails']

# ========== BRAND, MODEL, GENERATION, CATEGORY ==========
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name']

class CarModelSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)

    class Meta:
        model = CarModel
        fields = ['id', 'name', 'brand']

class GenerationSerializer(serializers.ModelSerializer):
    car_model = CarModelSerializer(read_only=True)

    class Meta:
        model = Generation
        fields = ['id', 'number', 'car_model']

class CarCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CarCategory
        fields = ['id', 'name']

# ========== CAR ==========
class CarSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    model = CarModelSerializer(read_only=True)
    generation = GenerationSerializer(read_only=True)
    category = CarCategorySerializer(read_only=True)

    class Meta:
        model = Car
        fields = [
            'id', 'license_plate', 'client', 'brand', 'model',
            'generation', 'category', 'year', 'fuel_type'
        ]

# ========== SERVICE CATEGORY ==========
class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['id', 'name']

# ========== PAYMENT ==========
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'method', 'amount', 'created_at']

# ========== SERVICE ==========
class ServiceSerializer(serializers.ModelSerializer):
    car = CarSerializer(read_only=True)
    category = ServiceCategorySerializer(many=True, read_only=True)
    payments = PaymentSerializer(source='payment_set', many=True, read_only=True)
    receipt_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = [
            'id', 'car', 'category', 'description', 'entry_date', 'delivery_time',
            'status', 'confirm_ready', 'labor_cost', 'parts_cost',
            'total_cost', 'total_paid', 'pending_amount',
            'is_paid', 'payment_confirmed_by_admin',
            'receipt_image_url', 'payments'
        ]

    def get_receipt_image_url(self, obj):
        if obj.receipt_image:
            return obj.receipt_image.url
        return None
