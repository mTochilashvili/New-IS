from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, DishViewSet, OrderItemViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'dishes', DishViewSet)
router.register(r'order-items', OrderItemViewSet)

urlpatterns = router.urls