from django.utils import timezone
from datetime import timedelta
from .models import Product, UserProfile, UserInteraction, Recommendation

class RecommendationEngine:
    """Classe para implementar algoritmos de recomendação"""
    
    def get_personalized_recommendations(self, user_id, max_items=10):
        """
        Gera recomendações personalizadas combinando métodos colaborativos 
        e baseados em conteúdo.
        """
        # Lógica para combinar recomendações colaborativas e baseadas em conteúdo
        # Na implementação real, você precisaria de algoritmos como matriz de fatoração
        # ou sistemas de filtragem colaborativa
        
        # Exemplo simples:
        collaborative_recs = self.get_collaborative_recommendations(user_id, max_items=max_items//2)
        content_recs = self.get_content_based_recommendations(user_id, max_items=max_items//2)
        
        # Combinar e remover duplicatas
        all_recs = {}
        for product_id, score in collaborative_recs:
            all_recs[product_id] = score
            
        for product_id, score in content_recs:
            if product_id in all_recs:
                all_recs[product_id] = (all_recs[product_id] + score) / 2  # Média dos scores
            else:
                all_recs[product_id] = score
        
        # Ordenar por score e limitar ao número desejado
        sorted_recs = sorted(all_recs.items(), key=lambda x: x[1], reverse=True)[:max_items]
        
        # Formatar resultados
        return [{"product_id": pid, "score": float(score)} for pid, score in sorted_recs]
    
    def get_collaborative_recommendations(self, user_id, max_items=10):
        """
        Gera recomendações baseadas em filtragem colaborativa (usuários semelhantes).
        """
        # Implementação simplificada para exemplo
        # Em produção, use algoritmos como Collaborative Filtering ou Matrix Factorization
        
        try:
            user_profile = UserProfile.objects.get(user_id=user_id)
            
            # Buscar produtos com os quais o usuário interagiu positivamente
            user_interactions = UserInteraction.objects.filter(
                user=user_profile,
                interaction_type__in=['purchase', 'favorite', 'rating']
            ).select_related('product')
            
            if not user_interactions:
                return self.get_trending_recommendations(max_items)
            
            # Pegar categorias que o usuário já demonstrou interesse
            categories = set()
            for interaction in user_interactions:
                categories.add(interaction.product.category)
            
            # Encontrar produtos populares nessas categorias que o usuário não interagiu
            user_product_ids = [i.product.product_id for i in user_interactions]
            
            # Produtos populares nas mesmas categorias
            popular_products = Product.objects.filter(
                category__in=categories
            ).exclude(
                product_id__in=user_product_ids
            )
            
            # Criar recomendações com scores simulados
            recommendations = []
            for i, product in enumerate(popular_products[:max_items]):
                score = 1.0 - (i * 0.05)  # Score simples decrescente
                recommendations.append((product.product_id, score))
                
            return recommendations
            
        except UserProfile.DoesNotExist:
            return self.get_trending_recommendations(max_items)
    
    def get_content_based_recommendations(self, user_id, max_items=10):
        """
        Gera recomendações baseadas no conteúdo/características dos produtos.
        """
        # Implementação simplificada para exemplo
        try:
            user_profile = UserProfile.objects.get(user_id=user_id)
            
            # Verificar se o usuário tem preferências
            if user_profile.preferences:
                preferred_categories = user_profile.preferences.get('categories', [])
                
                if preferred_categories:
                    # Recomendar produtos das categorias preferidas
                    products = Product.objects.filter(category__in=preferred_categories)[:max_items*2]
                    
                    # Criar recomendações com scores simulados
                    recommendations = []
                    for i, product in enumerate(products[:max_items]):
                        score = 1.0 - (i * 0.05)  # Score simples decrescente
                        recommendations.append((product.product_id, score))
                    
                    return recommendations
            
            # Fallback para recomendações de tendências
            return self.get_trending_recommendations(max_items)
            
        except UserProfile.DoesNotExist:
            return self.get_trending_recommendations(max_items)
    
    def get_trending_recommendations(self, max_items=10):
        """
        Retorna produtos populares/tendência como recomendação básica.
        """
        # Identificar produtos com mais interações recentes
        recent_cutoff = timezone.now() - timedelta(days=30)
        
        # Agregação para contar interações por produto
        from django.db.models import Count
        popular_products = Product.objects.filter(
            interactions__timestamp__gte=recent_cutoff
        ).annotate(
            interaction_count=Count('interactions')
        ).order_by('-interaction_count')[:max_items]
        
        # Criar recomendações com scores baseados na popularidade
        max_count = popular_products.first().interaction_count if popular_products else 1
        
        recommendations = []
        for product in popular_products:
            # Normalizar contagem para um score entre 0 e 1
            score = product.interaction_count / max_count
            recommendations.append((product.product_id, score))
        
        return recommendations
    
    def find_similar_products(self, product_id, max_items=10):
        """
        Encontra produtos similares a um produto específico.
        """
        try:
            product = Product.objects.get(product_id=product_id)
            
            # Encontrar produtos na mesma categoria
            similar_products = Product.objects.filter(
                category=product.category
            ).exclude(
                id=product.id
            )[:max_items*2]
            
            # Criar lista de produtos similares com scores
            result = []
            for i, similar in enumerate(similar_products[:max_items]):
                score = 1.0 - (i * 0.05)  # Score simples decrescente
                result.append({
                    "product_id": similar.product_id,
                    "score": score
                })
                
            return result
            
        except Product.DoesNotExist:
            return []