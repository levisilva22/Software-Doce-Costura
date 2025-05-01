from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    ProductViewSet,
    CartViewSet
)

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('product', ProductViewSet, basename='product')
router.register('cart', CartViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls)),
]