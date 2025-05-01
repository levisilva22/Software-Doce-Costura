from django.urls import path, include
from .views import ProductViewSet, UserProfileViewSet, UserInteractionViewSet, RecommendationViewSet
from rest_framework.routers import DefaultRouter

# Criar um router e registrar os ViewSets
router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'users', UserProfileViewSet)
router.register(r'interactions', UserInteractionViewSet)
router.register(r'recommendations', RecommendationViewSet)

# URLs da API
urlpatterns = [
    path('', include(router.urls)),
    
]