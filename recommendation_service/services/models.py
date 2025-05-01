from django.db import models
from django.utils import timezone

# Create your models here.

class Product(models.Model):
    """Modelo para armazenar informações básicas dos produtos"""
    product_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.product_id})"
    
    class Meta:
        indexes = [
            models.Index(fields=['product_id']),
            models.Index(fields=['category']),
        ]


class UserProfile(models.Model):
    """Modelo para armazenar perfis de usuários"""
    user_id = models.CharField(max_length=100, unique=True)
    preferences = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"User {self.user_id}"
    
    class Meta:
        indexes = [
            models.Index(fields=['user_id']),
        ]


class UserInteraction(models.Model):
    """Modelo para armazenar interações do usuário com produtos"""
    INTERACTION_TYPES = (
        ('view', 'Visualização'),
        ('click', 'Clique'),
        ('cart', 'Adicionado ao carrinho'),
        ('purchase', 'Compra'),
        ('rating', 'Avaliação'),
        ('favorite', 'Favorito'),
    )
    
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='interactions')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='interactions')
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES)
    rating = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    metadata = models.JSONField(default=dict, blank=True)
    
    def __str__(self):
        return f"{self.user} - {self.product} - {self.interaction_type}"
    
    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['product']),
            models.Index(fields=['interaction_type']),
            models.Index(fields=['timestamp']),
        ]


class Recommendation(models.Model):
    """Modelo para armazenar recomendações geradas para usuários"""
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='recommendations')
    products = models.JSONField()  # Lista de IDs de produtos recomendados com scores
    recommendation_type = models.CharField(max_length=50)  # ex: 'collaborative', 'content-based', 'personalized'
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Recomendação para {self.user} ({self.recommendation_type})"
    
    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['recommendation_type']),
            models.Index(fields=['is_active']),
        ]


class SimilarProducts(models.Model):
    """Modelo para armazenar produtos similares (pré-calculados)"""
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='similar_products')
    similar_items = models.JSONField()  # Lista de IDs de produtos similares com scores
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Produtos similares para {self.product}"
    
    class Meta:
        verbose_name_plural = "Similar Products"
