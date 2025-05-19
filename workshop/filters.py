import django_filters
from .models import Car, Client, Service, Brand, CarModel

class BrandFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Brand
        fields = ['name']

class CarModelFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    brand = django_filters.CharFilter(field_name='brand__name', lookup_expr='iexact')

    class Meta:
        model = CarModel
        fields = ['name', 'brand']

class CarFilter(django_filters.FilterSet):
    brand = django_filters.CharFilter(field_name='car_model__brand__name', lookup_expr='iexact')
    model = django_filters.CharFilter(field_name='car_model__name', lookup_expr='icontains')
    generation = django_filters.CharFilter(lookup_expr='iexact')
    fuel_type = django_filters.CharFilter(lookup_expr='iexact')
    license_plate = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Car
        fields = ['brand', 'model', 'generation', 'fuel_type', 'license_plate']

class ClientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    phone = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Client
        fields = ['name', 'phone']

class ServiceFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='iexact')
    entry_date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Service
        fields = ['category', 'entry_date']
