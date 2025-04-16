from django.urls import path
from .views import (
    CategoryViewSet,
    ProductViewSet,
)

urlpatterns = [
    path('category/', CategoryViewSet.as_view(), name = 'category'),
    path('product/', ProductViewSet.as_view(), name = 'product'),
]