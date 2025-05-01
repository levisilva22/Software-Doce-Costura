# api_gateway/gateway/urls.py
from django.urls import path, re_path
from .views import AuthProxyView, RecommendationView, ProductsView, PaymentProxyView

urlpatterns = [
    # Rotas de autenticação
    re_path(r'^auth/login/?$', AuthProxyView.as_view()),
    re_path(r'^auth/register/?$', AuthProxyView.as_view()),
    re_path(r'^auth/profile/?$', AuthProxyView.as_view()),
    re_path(r'^auth/refresh/?$', AuthProxyView.as_view()),
    re_path(r'^auth/verify/?$', AuthProxyView.as_view()),  # Verifica o token de autenticação

    # Rotas de recomendação
    re_path(r'^recommendations/?$', RecommendationView.as_view()),
    re_path(r'^recommendations/(?P<user_id>\d+)/?$', RecommendationView.as_view()),
    
    # Rotas de produtos
    re_path(r'^products/?$', ProductsView.as_view()),
    re_path(r'^products/(?P<product_id>\d+)/?$', ProductsView.as_view()),
    re_path(r'^products/categories/?$', ProductsView.as_view()),
    re_path(r'^products/product/?$', ProductsView.as_view()),

    re_path(r'payment/?$', PaymentProxyView.as_view()),
    re_path(r'productos/orders/?$', PaymentProxyView.as_view()),

]   