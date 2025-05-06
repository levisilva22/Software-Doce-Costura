import api from './api';

// Obter recomendações personalizadas para um usuário
export const getPersonalizedRecommendations = async (userId, limit = 10) => {
  const response = await api.get(`/recommendations/users/${userId}/recommendations`, {
    params: { limit }
  });
  return response.data;
};

// Obter produtos similares a um produto específico
export const getSimilarProducts = async (productId, limit = 6) => {
  const response = await api.get(`/recommendations/products/${productId}/similar_products`, {
    params: { limit }
  });
  return response.data;
};

// Obter produtos em tendência
export const getTrendingProducts = async (limit = 8) => {
  const response = await api.get('/recommendations/trending', {
    params: { limit }
  });
  return response.data;
};

// Obter produtos recém-chegados
export const getNewArrivals = async (limit = 8, days = 30) => {
  const response = await api.get('/recommendations/new_arrivals', {
    params: { limit, days }
  });
  return response.data;
};

// Registrar uma interação do usuário com um produto
export const trackUserInteraction = async (data) => {
  const response = await api.post('/recommendations/interactions', data);
  return response.data;
};

// Tipos de interações para uso no frontend
export const InteractionTypes = {
  VIEW: 'view',
  CLICK: 'click',
  ADD_TO_CART: 'add_to_cart',
  PURCHASE: 'purchase',
  RATE: 'rate',
  FAVORITE: 'favorite',
  SEARCH: 'search'
};