import { useCallback } from 'react';
import { trackUserInteraction } from '../services/recommendationService';
import { useAuth } from '../contexts/AuthContext';

export function useTrackInteraction() {
  const { isAuthenticated } = useAuth();
  
  const trackInteraction = useCallback((productId, interactionType, metadata = {}) => {
    // Só rastreia se o usuário estiver autenticado
    if (isAuthenticated && productId) {
      // Executa de forma assíncrona sem esperar resposta
      trackUserInteraction(productId, interactionType, metadata);
    }
  }, [isAuthenticated]);
  
  return trackInteraction;
}