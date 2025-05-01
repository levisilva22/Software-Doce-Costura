from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    
    # Campos para auditoria - sem relação direta com User
    creator_id = models.IntegerField(null=True, blank=True)  # ID do usuário que criou
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_modified_by = models.IntegerField(null=True, blank=True)  # ID do usuário que modificou por último
    
    # Campos específicos para o negócio
    sku = models.CharField(max_length=50, unique=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
        
    # Métodos específicos do domínio de produto
    def is_in_stock(self):
        return self.stock > 0
        
    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk': self.pk})

class Cart(models.Model):
    user_id = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Cart of user {self.user_id}" 
    
    class Meta:
        indexes = [
                models.Index(fields=('user_id', 'is_active')), 
        ]
        
    @property
    def subtotal(self):
        """Calcula o valor total dos itens no carrinho"""
        return sum(item.line_total for item in self.items.all())
        
    @property
    def total_items(self):
        """Retorna o número total de itens no carrinho"""
        return self.items.count()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('cart', 'product')
        
    @property
    def line_total(self):
        """Calcula o preço total deste item (quantidade * preço)"""
        return self.quantity * self.product.price