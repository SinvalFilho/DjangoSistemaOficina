from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Client, Car, Generation, Service, ServiceCategory, Brand, CarModel
from .serializers import (
    ClientSerializer, CarSerializer, GenerationSerializer,
    ServiceSerializer, ServiceCategorySerializer,
    BrandSerializer, CarModelSerializer
)
from .filters import ClientFilter, CarFilter, ServiceFilter, BrandFilter, CarModelFilter
from .permissions import RequireSuperuserConfirmation


# -----------------------------
# ViewSets
# -----------------------------

class ClientViewSet(viewsets.ModelViewSet):
    """
    Endpoints: /clients/
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [RequireSuperuserConfirmation]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ClientFilter


class CarViewSet(viewsets.ModelViewSet):
    """
    Endpoints: /cars/
    """
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [RequireSuperuserConfirmation]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CarFilter


class GenerationViewSet(viewsets.ModelViewSet):
    """
    Endpoints: /generations/
    """
    queryset = Generation.objects.all()
    serializer_class = GenerationSerializer
    permission_classes = [RequireSuperuserConfirmation]


class BrandViewSet(viewsets.ModelViewSet):
    """
    Endpoints: /brands/
    """
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [RequireSuperuserConfirmation]
    filter_backends = [DjangoFilterBackend]
    filterset_class = BrandFilter


class CarModelViewSet(viewsets.ModelViewSet):
    """
    Endpoints: /car-models/
    """
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer
    permission_classes = [RequireSuperuserConfirmation]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CarModelFilter


class ServiceCategoryViewSet(viewsets.ModelViewSet):
    """
    Endpoints: /service-categories/
    """
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes = [RequireSuperuserConfirmation]


class ServiceViewSet(viewsets.ModelViewSet):
    """
    Endpoints: /services/
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ServiceFilter

    def get_permissions(self):
        # Superuser confirmation required for updates and deletes
        if self.action in ['update', 'partial_update', 'destroy']:
            return [RequireSuperuserConfirmation()]
        return super().get_permissions()


# -----------------------------
# Payment Confirmation View
# -----------------------------

class ConfirmPaymentView(APIView):
    """
    Endpoint: POST /services/{pk}/confirm-payment/
    Only superusers may confirm full payment and mark a service as paid.
    """
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        service = get_object_or_404(Service, pk=pk)
        if not service.check_if_fully_paid():
            return Response({'detail': 'Pagamento incompleto. Não é possível concluir.'}, status=400)
        service.is_paid = True
        service.payment_confirmed_by_admin = True
        service.save()
        return Response({'detail': 'Pagamento confirmado.'})
