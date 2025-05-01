from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    ProfileView,
    TokenValidationView,
    ChangePasswordView,
    RefreshTokenView
)

urlpatterns = [
    # Autenticação básica
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify/', TokenValidationView.as_view(), name='verify_token'),
    # Perfil de usuário
    path('profile/', ProfileView.as_view(), name='profile'),
    
    # Gerenciamento de senha
    path('password/change/', ChangePasswordView.as_view(), name='change_password'),
    
    # Gerenciamento de tokens
    path('token/validate/', TokenValidationView.as_view(), name='validate_token'),
    path('token/refresh/', RefreshTokenView.as_view(), name='refresh_token'),
]


