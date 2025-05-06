import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

function PrivateRoute({ children }) {
  const { signed, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return <div>Carregando...</div>;
  }

  if (!signed) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
}

export default PrivateRoute;
