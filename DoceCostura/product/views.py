from django.shortcuts import render
from rest_framework import viewsets, filters, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category, Cart, CartItem
from .permissions import MicroservicePermission
from .serializers import (
    ProductSerializer,
    ProductListSerializer, 
    CategorySerializer,
    CartSerializer
)

# Permissão personalizada para permitir apenas superusuários
class IsSuperUserOrMicroservice(permissions.BasePermission):
    def has_permission(self, request, view):
        # Permitir superusuários do Django
        if request.user and request.user.is_authenticated and request.user.is_superuser:
            return True
        # Manter compatibilidade com o middleware JWT se necessário
        if hasattr(request, 'user_data'):
            roles = request.user_data.get('roles', [])
            return 'is_superuser' in roles
        return False

class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar categorias de produtos.
    ViewSet realiza as operações de CRUD.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [MicroservicePermission]
    filter_backends = [filters.SearchFilter] # Adiciona filtro de pesquisa
    search_fields = ['name']


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar produtos.
    GET, POST, PUT, PATCH, DELETE para produtos.
    """
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [IsSuperUserOrMicroservice]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_featured']
    search_fields = ['name', 'description', 'sku']
    ordering_fields = ['price', 'name', 'created_at']
    
    def get_serializer_class(self):
        """
        Use different serializers for different actions:
        - list: ProductListSerializer (lightweight)
        - retrieve, create, update: ProductSerializer (full details)
        """
        if self.action == 'list':
            return ProductListSerializer
        return ProductSerializer
    
    def perform_create(self, serializer):
        """
        Adiciona o ID do criador ao produto quando é criado.
        """
        # Para super usuários do Django, use o ID do usuário
        if self.request.user and self.request.user.is_authenticated:
            creator_id = self.request.user.id
        # Fallback para user_data se disponível (compatibilidade com middleware JWT)
        elif hasattr(self.request, 'user_data'):
            creator_id = self.request.user_data.get('id', 1)
        else:
            # Valor padrão para testes ou quando não há autenticação
            creator_id = 1
            
        serializer.save(creator_id=creator_id)
    
    def perform_update(self, serializer):
        """
        Adiciona o ID do último modificador quando o produto é atualizado.
        """
        # Para super usuários do Django, use o ID do usuário
        if self.request.user and self.request.user.is_authenticated:
            modifier_id = self.request.user.id
        # Fallback para user_data se disponível (compatibilidade com middleware JWT)
        elif hasattr(self.request, 'user_data'):
            modifier_id = self.request.user_data.get('id', 1)
        else:
            # Valor padrão para testes ou quando não há autenticação
            modifier_id = 1
            
        serializer.save(last_modified_by=modifier_id)
    
    @action(detail=True, methods=['post'])
    def toggle_featured(self, request, pk=None):
        """
        Endpoint personalizado para ativar/desativar destaque de um produto.
        """
        product = self.get_object()
        product.is_featured = not product.is_featured
        product.save()
        serializer = self.get_serializer(product)
        return Response(serializer.data) 
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """
        Endpoint para listar apenas produtos em destaque.
        """
        featured_products = Product.objects.filter(is_featured=True, is_active=True)
        page = self.paginate_queryset(featured_products)
        
        if page is not None:
            serializer = ProductListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = ProductListSerializer(featured_products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """
        Endpoint para listar produtos agrupados por categoria.
        """
        categories = Category.objects.all()
        result = []
        
        for category in categories:
            products = Product.objects.filter(
                category=category, 
                is_active=True
            )[:10]  # Limita a 10 produtos por categoria
            
            if products.exists():
                category_data = CategorySerializer(category).data
                products_data = ProductListSerializer(products, many=True).data
                result.append({
                    'category': category_data,
                    'products': products_data
                })
        
        return Response(result)
    
    @action(detail=True, methods=['post'])
    def update_stock(self, request, pk=None):
        """
        Endpoint para atualizar o estoque de um produto.
        Requer autenticação de superusuário.
        """
        product = self.get_object()
        quantity = request.data.get('quantity', 0)
        
        # Verificação simplificada - já verificado pela permissão da classe
        if not isinstance(quantity, int):
            return Response(
                {'error': 'A quantidade deve ser um número inteiro'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        product.stock += quantity
        
        if product.stock < 0:
            return Response(
                {'error': 'Estoque insuficiente para esta operação'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        product.save()
        serializer = self.get_serializer(product)
        return Response(serializer.data)


class CartViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar o carrinho de compras.
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [MicroservicePermission]

    def get_queryset(self):
        """
        Retorna apenas o carrinho do usuário atual.
        """
        user_id = self.request.user_data.get('id')
        if user_id:
            return Cart.objects.filter(user_id=user_id, is_active=True)
        return Cart.objects.none()

    def create(self, request, *args, **kwargs):
        """
        Cria um novo carrinho para o usuário se não existir.
        """
        user_id = request.user_data.get('id')
        if not user_id:
            return Response(
                {"error": "Usuário não autenticado"}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        # Verificar se o usuário já tem um carrinho ativo
        existing_cart = Cart.objects.filter(user_id=user_id, is_active=True).first()
        if existing_cart:
            serializer = self.get_serializer(existing_cart)
            return Response(serializer.data)
            
        # Criar um novo carrinho
        cart = Cart.objects.create(user_id=user_id)
        serializer = self.get_serializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def add_item(self, request):
        """
        Adiciona um produto ao carrinho ou atualiza sua quantidade.
        """
        user_id = request.user_data.get('id')
        if not user_id:
            return Response(
                {"error": "Usuário não autenticado"}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        # Obter ou criar o carrinho do usuário
        cart, created = Cart.objects.get_or_create(
            user_id=user_id, 
            is_active=True
        )
        
        # Validar produto
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        
        try:
            product = Product.objects.get(id=product_id, is_active=True)
        except Product.DoesNotExist:
            return Response(
                {"error": "Produto não encontrado"}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        # Verificar estoque
        if product.stock < quantity:
            return Response(
                {"error": "Quantidade solicitada não disponível em estoque"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Adicionar ou atualizar item no carrinho
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            # Se o item já existir, atualiza a quantidade
            cart_item.quantity += quantity
            
            # Verificar estoque novamente após aumentar quantidade
            if product.stock < cart_item.quantity:
                return Response(
                    {"error": "Quantidade solicitada não disponível em estoque"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            cart_item.save()
            
        # Atualizar timestamp do carrinho
        cart.save()
        
        serializer = self.get_serializer(cart)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def update_item(self, request):
        """
        Atualiza a quantidade de um item no carrinho.
        """
        user_id = self.request.user_data.get('id')
        if not user_id:
            return Response(
                {"error": "Usuário não autenticado"}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        
        # Validar quantidade
        if quantity < 0:
            return Response(
                {"error": "A quantidade deve ser maior ou igual a zero"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            cart = Cart.objects.get(user_id=user_id, is_active=True)
        except Cart.DoesNotExist:
            return Response(
                {"error": "Carrinho não encontrado"}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        try:
            product = Product.objects.get(id=product_id, is_active=True)
        except Product.DoesNotExist:
            return Response(
                {"error": "Produto não encontrado"}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        # Se quantidade for zero, remover item
        if quantity == 0:
            CartItem.objects.filter(cart=cart, product=product).delete()
        else:
            # Verificar estoque
            if product.stock < quantity:
                return Response(
                    {"error": "Quantidade solicitada não disponível em estoque"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            # Atualizar ou criar item
            cart_item, created = CartItem.objects.update_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )
        
        # Atualizar timestamp do carrinho
        cart.save()
        
        serializer = self.get_serializer(cart)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        """
        Remove um produto do carrinho.
        """
        user_id = self.request.user_data.get('id')
        if not user_id:
            return Response(
                {"error": "Usuário não autenticado"}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        product_id = request.data.get('product_id')
        
        try:
            cart = Cart.objects.get(user_id=user_id, is_active=True)
        except Cart.DoesNotExist:
            return Response(
                {"error": "Carrinho não encontrado"}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        # Remover item
        deleted, _ = CartItem.objects.filter(
            cart=cart, 
            product_id=product_id
        ).delete()
        
        if deleted == 0:
            return Response(
                {"error": "Item não encontrado no carrinho"}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        # Atualizar timestamp do carrinho
        cart.save()
        
        serializer = self.get_serializer(cart)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def clear(self, request):
        """
        Remove todos os itens do carrinho.
        """
        user_id = self.request.user_data.get('id')
        if not user_id:
            return Response(
                {"error": "Usuário não autenticado"}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        try:
            cart = Cart.objects.get(user_id=user_id, is_active=True)
        except Cart.DoesNotExist:
            return Response(
                {"error": "Carrinho não encontrado"}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        # Remover todos os itens
        cart.items.all().delete()
        
        # Atualizar timestamp do carrinho
        cart.save()
        
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

