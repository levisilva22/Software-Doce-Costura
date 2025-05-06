import React, { createContext, useState, useContext, useEffect, useCallback } from 'react';
import { validateToken, login as loginService, refreshToken } from '../services/authService';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  
  const logout = useCallback(() => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
    setUser(null);
  }, []);

  const login = useCallback(async (credentials) => {
    try {
      const data = await loginService(credentials);
      
      // Armazena o token
      localStorage.setItem('token', data.token);
      
      // Extrai os dados do usuário da resposta
      const userData = {
        id: data.user_id,
        email: data.email,
        username: data.username,
        firstName: data.first_name || '',
        lastName: data.last_name || ''
      };
      
      // Atualiza estado
      setUser(userData);
      setIsAuthenticated(true);
      return userData;
    } catch (error) {
      console.error('Erro ao fazer login:', error);
      throw error;
    }
  }, []);

  const refreshUserToken = useCallback(async () => {
    try {
      const data = await refreshToken();
      localStorage.setItem('token', data.token);
      return true;
    } catch (error) {
      console.error('Erro ao atualizar token:', error);
      logout();
      return false;
    }
  }, [logout]);

  const checkAuthStatus = useCallback(async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      
      if (!token) {
        setLoading(false);
        return;
      }

      try {
        const data = await validateToken();
        
        setUser({
          id: data.user_id,
          email: data.email,
          username: data.username,
          firstName: data.first_name || '',
          lastName: data.last_name || ''
        });
        
        setIsAuthenticated(true);
      } catch (error) {
        // Se o token expirou mas ainda é válido para refresh
        if (error.response && error.response.status === 401) {
          const refreshSuccess = await refreshUserToken();
          if (!refreshSuccess) {
            logout();
          }
        } else {
          // Outros erros
          logout();
        }
      }
    } finally {
      setLoading(false);
    }
  }, [logout, refreshUserToken]);

  useEffect(() => {
    checkAuthStatus();
  }, [checkAuthStatus]);

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated,
        user,
        loading,
        login,
        logout,
        refreshUserToken,
        checkAuthStatus
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
