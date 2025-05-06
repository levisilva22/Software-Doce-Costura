from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
import uuid


class CustomUserManager(BaseUserManager):
    """
    Gerenciador de modelo de usuário personalizado onde o email é o identificador único
    para autenticação em vez de nomes de usuário.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Cria e salva um usuário com o email e senha fornecidos.
        """
        if not email:
            raise ValueError(_('O email é obrigatório'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Cria e salva um superusuário com o email e senha fornecidos.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superusuário deve ter is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superusuário deve ter is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Modelo de usuário personalizado para o microserviço de autenticação,
    usando email como identificador único.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    # Campos para rastreamento
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    
    # Campos específicos para microserviços
    external_id = models.CharField(max_length=100, blank=True, null=True, help_text="ID em sistemas externos")
    
    # Preferências e configurações
    preferences = models.JSONField(default=dict, blank=True)
    
    # Configure o username como o campo para login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        
    def __str__(self):
        return self.email


class UserProfile(models.Model):
    """
    Modelo para armazenar informações adicionais sobre o usuário
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return f"Perfil de {self.user.username}"


class Device(models.Model):
    """
    Modelo para rastrear dispositivos usados para login
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    device_id = models.CharField(max_length=255)
    device_name = models.CharField(max_length=255)
    device_type = models.CharField(max_length=50)  # mobile, desktop, tablet, etc.
    last_login = models.DateTimeField(auto_now=True)
    is_trusted = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('user', 'device_id')
    
    def __str__(self):
        return f"{self.device_name} de {self.user.email}"


