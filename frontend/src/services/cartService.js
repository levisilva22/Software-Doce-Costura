import api from './api';

export const getCart = async () => {
  const response = await api.get('/cart/');
  return response.data;
};

export const addToCart = async (productId, quantity = 1) => {
  const response = await api.post('/cart/items/', { product_id: productId, quantity });
  return response.data;
};

export const updateCartItem = async (itemId, quantity) => {
  const response = await api.put(`/cart/items/${itemId}/`, { quantity });
  return response.data;
};

export const removeCartItem = async (itemId) => {
  const response = await api.delete(`/cart/items/${itemId}/`);
  return response.data;
};

export const clearCart = async () => {
  const response = await api.delete('/cart/items/');
  return response.data;
};

export const applyPromoCode = async (promoCode) => {
  const response = await api.post('/cart/promo/', { code: promoCode });
  return response.data;
};