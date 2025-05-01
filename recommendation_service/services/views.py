from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta

from .models import Product, UserProfile, UserInteraction, Recommendation, SimilarProducts
from .serializers import (
    ProductSerializer,
    UserProfileSerializer, 
    UserInteractionSerializer, 
    RecommendationSerializer,
    SimilarProductsSerializer
)
from .recommendation_engine import RecommendationEngine

# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet para operações CRUD em produtos"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'category', 'description']
    
    @action(detail=True, methods=['get'])
    def similar_products(self, request, pk=None):
        """Retorna produtos similares para um produto específico"""
        product = self.get_object()
        
        try:
            similar_products = SimilarProducts.objects.get(product=product)
            return Response(similar_products.similar_items)
        except SimilarProducts.DoesNotExist:
            # Gerar similaridades sob demanda se não existirem
            recommendation_engine = RecommendationEngine()
            similar_items = recommendation_engine.find_similar_products(product.product_id)
            
            # Opcional: salvar para uso futuro
            SimilarProducts.objects.create(
                product=product,
                similar_items=similar_items
            )
            
            return Response(similar_items)


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet para operações CRUD em perfis de usuário"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    
    @action(detail=True, methods=['get'])
    def recommendations(self, request, pk=None):
        """Retorna recomendações para um usuário específico"""
        user_profile = self.get_object()
        recommendation_type = request.query_params.get('type', 'personalized')
        max_items = int(request.query_params.get('max_items', 10))
        
        # Verificar se existem recomendações válidas em cache
        current_time = timezone.now()
        cached_recommendations = Recommendation.objects.filter(
            user=user_profile,
            recommendation_type=recommendation_type,
            is_active=True,
            expires_at__gt=current_time
        ).first()
        
        if cached_recommendations:
            # Limitar ao número solicitado de itens
            products = cached_recommendations.products[:max_items]
            return Response(products)
        else:
            # Gerar novas recomendações
            recommendation_engine = RecommendationEngine()
            
            if recommendation_type == 'personalized':
                recommended_products = recommendation_engine.get_personalized_recommendations(
                    user_profile.user_id, 
                    max_items=max_items
                )
            elif recommendation_type == 'collaborative':
                recommended_products = recommendation_engine.get_collaborative_recommendations(
                    user_profile.user_id,
                    max_items=max_items
                )
            elif recommendation_type == 'content-based':
                recommended_products = recommendation_engine.get_content_based_recommendations(
                    user_profile.user_id,
                    max_items=max_items
                )
            else:
                recommended_products = recommendation_engine.get_trending_recommendations(
                    max_items=max_items
                )
            
            # Salvar recomendações no banco para uso futuro
            Recommendation.objects.create(
                user=user_profile,
                products=recommended_products,
                recommendation_type=recommendation_type,
                expires_at=current_time + timedelta(hours=24)  # Expira em 24 horas
            )
            
            return Response(recommended_products)


class UserInteractionViewSet(viewsets.ModelViewSet):
    """ViewSet para registrar interações de usuário"""
    queryset = UserInteraction.objects.all()
    serializer_class = UserInteractionSerializer
    
    def create(self, request, *args, **kwargs):
        """Registra uma nova interação de usuário e atualiza recomendações"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Opcionalmente, invalidar recomendações em cache
        # para forçar recálculo na próxima solicitação
        if serializer.validated_data.get('interaction_type') in ['purchase', 'rating']:
            Recommendation.objects.filter(
                user=serializer.validated_data['user'],
                is_active=True
            ).update(is_active=False)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RecommendationViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciar recomendações"""
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer
    
    @action(detail=False, methods=['get'])
    def trending(self, request):
        """Retorna produtos em tendência"""
        max_items = int(request.query_params.get('max_items', 10))
        recommendation_engine = RecommendationEngine()
        trending_products = recommendation_engine.get_trending_recommendations(max_items=max_items)
        return Response(trending_products)

    @action(detail=False, methods=['get'])
    def new_arrivals(self, request):
        """Retorna produtos recém adicionados"""
        max_items = int(request.query_params.get('max_items', 10))
        days = int(request.query_params.get('days', 30))
        
        # Buscar produtos adicionados nos últimos "days" dias
        cutoff_date = timezone.now() - timedelta(days=days)
        new_products = Product.objects.filter(
            created_at__gte=cutoff_date
        ).order_by('-created_at')[:max_items]
        
        serializer = ProductSerializer(new_products, many=True)
        return Response(serializer.data)
