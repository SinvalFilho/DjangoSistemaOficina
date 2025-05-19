from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ClientViewSet, CarViewSet, GenerationViewSet,
    ServiceViewSet, ServiceCategoryViewSet,
    BrandViewSet, CarModelViewSet, ConfirmPaymentView
)

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'cars', CarViewSet)
router.register(r'generations', GenerationViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'service-categories', ServiceCategoryViewSet)
router.register(r'brands', BrandViewSet)
router.register(r'car-models', CarModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(
        'services/<int:pk>/confirm-payment/',
        ConfirmPaymentView.as_view(),
        name='service-confirm-payment'
    ),
]