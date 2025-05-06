import api from './api';

export const getProducts = async (params) => {
  const response = await api.get('/products/', { params });
  return response.data;
};

export const getProductById = async (id) => {
  const response = await api.get(`/products/${id}/`);
  return response.data;
};

export const getCategories = async () => {
  const response = await api.get('/products/categories/');
  return response.data;
};

export const searchProducts = async (query) => {
  const response = await api.get('/products/search/', { params: { q: query } });
  return response.data;
};

export const getFeaturedProducts = async () => {
  const response = await api.get('/products/featured/');
  return response.data;
};

// Para o Admin - requer autenticação
export const createProduct = async (productData) => {
  const response = await api.post('/products/', productData);
  return response.data;
};

export const updateProduct = async (id, productData) => {
  const response = await api.put(`/products/${id}/`, productData);
  return response.data;
};

export const deleteProduct = async (id) => {
  const response = await api.delete(`/products/${id}/`);
  return response.data;
};
