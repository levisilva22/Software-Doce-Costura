import axios from 'axios';
import { toast } from 'react-toastify';

// URL do API Gateway
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  timeout: 15000,
});

// Interceptor para adicionar token em todas as requisições
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Interceptor para tratamento global de erros
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Define uma mensagem de erro padrão
    let errorMessage = 'Ocorreu um erro inesperado';

    if (error.response) {
      // O servidor retornou um status de erro
      const { status } = error.response;
      
      if (status === 401) {
        // Token inválido ou expirado
        localStorage.removeItem('token');
        errorMessage = 'Sua sessão expirou. Por favor, faça login novamente.';
        
        // Redireciona para login apenas se não estiver já na página de login
        if (!window.location.pathname.includes('login')) {
          window.location.href = '/login';
        }
      } else if (status === 403) {
        errorMessage = 'Você não tem permissão para acessar este recurso';
      } else if (status === 404) {
        errorMessage = 'Recurso não encontrado';
      } else if (status === 500) {
        errorMessage = 'Erro interno do servidor. Por favor, tente novamente mais tarde.';
      }
      
      // Usa a mensagem da API se disponível
      if (error.response.data && error.response.data.message) {
        errorMessage = error.response.data.message;
      }
    } else if (error.request) {
      // A requisição foi feita mas não houve resposta
      errorMessage = 'Não foi possível conectar ao servidor. Verifique sua conexão.';
    }
    
    // Exibe mensagem de erro (exceto em rotas de autenticação onde o erro é tratado localmente)
    if (!error.config.url.includes('/auth/')) {
      toast.error(errorMessage);
    }
    
    return Promise.reject(error);
  }
);

export default api;
