import { useCallback } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { trackUserInteraction, InteractionTypes } from '../services/recommendationService';

export const useInteractionTracker = () => {
  const { isAuthenticated, user } = useAuth();
  
  const trackInteraction = useCallback(async (productId, interactionType, metadata = {}) => {
    try {
      if (!isAuthenticated || !user) {
        // Usuário anônimo - pode-se implementar rastreamento anônimo se necessário
        return;
      }
      
      await trackUserInteraction({
        user_id: user.id,
        product_id: productId,
        interaction_type: interactionType,
        ...metadata
      });
    } catch (error) {
      // Apenas log, não exibimos erro para o usuário quando falha o rastreamento
      console.error('Erro ao rastrear interação:', error);
    }
  }, [isAuthenticated, user]);

  return {
    viewProduct: (productId) => trackInteraction(productId, InteractionTypes.VIEW),
    clickProduct: (productId) => trackInteraction(productId, InteractionTypes.CLICK),
    addToCart: (productId, quantity) => 
      trackInteraction(productId, InteractionTypes.ADD_TO_CART, { quantity }),
    purchaseProduct: (productId, quantity, price) => 
      trackInteraction(productId, InteractionTypes.PURCHASE, { quantity, price }),
    rateProduct: (productId, rating) => 
      trackInteraction(productId, InteractionTypes.RATE, { rating }),
    favoriteProduct: (productId, isFavorite) => 
      trackInteraction(productId, InteractionTypes.FAVORITE, { is_favorite: isFavorite }),
    searchProduct: (query) => 
      trackInteraction(null, InteractionTypes.SEARCH, { query })
  };
};