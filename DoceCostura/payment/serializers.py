# serializers.py
from rest_framework import serializers
from .models import Order, OrderItem, Payment

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product_id', 'product_name', 'quantity', 'price', 'total']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'status', 'created_at', 
            'shipping_address', 'shipping_city', 'shipping_state', 'shipping_zipcode',
            'subtotal', 'shipping_fee', 'discount', 'total',
            'payment_method', 'paid_at', 'items'
        ]

class PaymentSerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(source='order.order_number', read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'order', 'order_number', 'amount', 'payment_method',
            'status', 'transaction_id', 'transaction_data',
            'created_at', 'updated_at'
        ]

class PaymentDetailSerializer(serializers.Serializer):
    # Campos para cartão de crédito
    card_number = serializers.CharField(required=False)
    card_holder = serializers.CharField(required=False)
    expiry_date = serializers.CharField(required=False)
    cvv = serializers.CharField(required=False)
    
    # Para outros métodos, adicione campos específicos

class CheckoutSerializer(serializers.Serializer):
    address = serializers.CharField()
    city = serializers.CharField()
    state = serializers.CharField(max_length=2)
    zipcode = serializers.CharField(max_length=9)
    payment_method = serializers.ChoiceField(choices=Order.PAYMENT_METHODS)
    shipping_fee = serializers.DecimalField(max_digits=6, decimal_places=2, required=False, default=0)
    discount = serializers.DecimalField(max_digits=6, decimal_places=2, required=False, default=0)
    payment_details = PaymentDetailSerializer(required=False)