from rest_framework import serializers
from .models import Product, Category, CartItem, Cart

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class ProductSerializer(serializers.ModelSerializer):
    # Opcional: Incluir a categoria como objeto aninhado
    category_details = CategorySerializer(source='category', read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'stock', 
            'category', 'category_details', 'image', 
            'creator_id', 'created_at', 'updated_at', 
            'last_modified_by', 'sku', 'is_featured', 'is_active'
        ]
        read_only_fields = [
            'id', 'creator_id', 'created_at', 
            'updated_at', 'last_modified_by'
        ]
        extra_kwargs = {
            'category': {'write_only': True}  # Opcional: se quiser que apenas category_id seja enviado em POST/PUT
        }
    
    def validate_price(self, value):
        """Validação personalizada para o preço"""
        if value <= 0:
            raise serializers.ValidationError("O preço deve ser maior que zero.")
        return value
    
    def validate_stock(self, value):
        """Validação personalizada para o estoque"""
        if value < 0:
            raise serializers.ValidationError("O estoque não pode ser negativo.")
        return value

# Serializer para listagens (versão mais leve)
class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image', 'is_featured', 'category_name']

# Serializer para adição rápida ao carrinho
class ProductMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductMinimalSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True,
        source='product'
    )
    line_total = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        read_only=True
    )
    
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'line_total', 'added_at']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    subtotal = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        read_only=True
    )
    total_items = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'user_id', 'items', 'subtotal', 'total_items', 
                  'created_at', 'updated_at', 'is_active']
        read_only_fields = ['user_id', 'created_at', 'updated_at']