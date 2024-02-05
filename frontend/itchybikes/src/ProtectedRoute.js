// ProtectedRoute.js
import React from 'react';
import { Navigate, Route } from 'react-router-dom';
import { useAuth } from './AuthContext';

const ProtectedRoute = ({ element, ...props }) => {
  const { isAuthenticated } = useAuth();

  return isAuthenticated ? (
    <Route {...props} element={element} />
  ) : (
    <Navigate to="/login" />
  );
};

export default ProtectedRoute;
