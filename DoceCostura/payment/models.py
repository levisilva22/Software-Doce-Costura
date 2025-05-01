from decimal import Decimal
from django.db import models
from django.utils import timezone

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pendente'),
        ('paid', 'Pago'),
        ('processing', 'Em processamento'),
        ('shipped', 'Enviado'),
        ('delivered', 'Entregue'),
        ('cancelled', 'Cancelado'),
        ('refunded', 'Reembolsado'),
    )
    
    PAYMENT_METHODS = (
        ('credit_card', 'Cartão de Crédito'),
        ('debit_card', 'Cartão de Débito'),
        ('pix', 'PIX'),
        ('bank_transfer', 'Transferência Bancária'),
        ('boleto', 'Boleto'),
    )
    
    user_id = models.IntegerField()
    order_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Endereço de entrega
    shipping_address = models.TextField()
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=2)
    shipping_zipcode = models.CharField(max_length=9)
    
    # Valores
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Pagamento
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    payment_id = models.CharField(max_length=100, blank=True, null=True)  # ID da transação no gateway
    paid_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Order #{self.order_number}"
    
    def save(self, *args, **kwargs):
        # Gerar número do pedido se não existir
        if not self.order_number:
            self.order_number = self._generate_order_number()
            
        # Calcular total se não definido
        if not self.total:
            self.total = self.subtotal + self.shipping_fee - self.discount
            
        super().save(*args, **kwargs)
    
    def _generate_order_number(self):
        # Cria um número de pedido único baseado na data e ID
        timestamp = timezone.now().strftime('%Y%m%d%H%M')
        random_suffix = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        return f"{timestamp}{random_suffix}"
    
    def mark_as_paid(self, payment_id):
        self.status = 'paid'
        self.payment_id = payment_id
        self.paid_at = timezone.now()
        self.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=100)  # Armazenamos o nome para preservar histórico
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Preço unitário no momento da compra
    
    @property
    def total(self):
        return self.price * self.quantity

class Payment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pendente'),
        ('approved', 'Aprovado'),
        ('declined', 'Recusado'),
        ('refunded', 'Reembolsado'),
        ('cancelled', 'Cancelado'),
    )
    
    order = models.ForeignKey(Order, related_name='payments', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=Order.PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    transaction_data = models.JSONField(default=dict)  # Armazena resposta do gateway
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Payment {self.transaction_id} for Order #{self.order.order_number}"
