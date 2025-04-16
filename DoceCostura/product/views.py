from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category
from .serializers import (
    ProductSerializer,
    ProductListSerializer, 
    CategorySerializer,
    ProductMinimalSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar categorias de produtos.
    ViewSet realiza as operações de CRUD.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter] # Adiciona filtro de pesquisa
    search_fields = ['name']


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar produtos.
    GET, POST, PUT, PATCH, DELETE para produtos.
    """
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
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
        # Em um microserviço real, este ID viria do token JWT
        # Por enquanto, vamos usar um valor fixo para teste
        creator_id = getattr(self.request.user, 'id', 1)  # Valor padrão 1 para testes
        serializer.save(creator_id=creator_id)
    
    def perform_update(self, serializer):
        """
        Adiciona o ID do último modificador quando o produto é atualizado.
        """
        modifier_id = getattr(self.request.user, 'id', 1)  # Valor padrão 1 para testes
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
        Requer autenticação.
        """
        product = self.get_object()
        quantity = request.data.get('quantity', 0)
        
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
