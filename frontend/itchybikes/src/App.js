// Import Navigate from react-router-dom
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import React from 'react';
import Home from './components/Home';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import SignUpPage from './pages/SignUpPage';
import Header from './components/common/Header';
import Profile from './components/Profile';
import { useNavigate } from 'react-router-dom';
import { AuthProvider } from './AuthContext';
import ProtectedRoute from './ProtectedRoute';
import './App.css';

// A simple example of a higher-order component for private routes
const PrivateRoute = ({ element, ...props }) => {
  const isAuthenticated = localStorage.getItem('accessToken'); // Check if the user is authenticated
  const navigate = useNavigate(); // Make sure useNavigate is used at the top level

  return isAuthenticated ? element : <Navigate to="/login" />;
};

const App = () => {
  return (
    <AuthProvider>
    <Router>
      <Routes>
        <Route
          path="/"
          element={
            <div>
              <Header />
              <Home />
            </div>
          }
        />
        <Route path="/" element={<Header />} />
        <Route path="/home" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignUpPage />} />
        <Route
          path="/profile"
          element={<PrivateRoute element={<Profile />} />}
        />
      </Routes>
    </Router>
    </AuthProvider>
  );
};

export default App;
