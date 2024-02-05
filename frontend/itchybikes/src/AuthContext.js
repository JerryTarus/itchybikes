import React, { createContext, useContext, useState } from 'react';

// Create the AuthContext
const AuthContext = createContext();

// Create a hook to use the AuthContext
export const useAuth = () => {
  return useContext(AuthContext);
};

// Create the AuthProvider component
export const AuthProvider = ({ children }) => {
  // State to keep track of the user's authentication status
  const [isAuthenticated, setAuthenticated] = useState(false);

  // Function to perform login
  const login = async (email, password) => {
    try {
      // Perform your authentication logic here
      // For example, make a request to your backend
      // and set isAuthenticated to true if authentication is successful
      // Replace the following logic with your actual authentication process
      if (email === 'example@email.com' && password === 'password123') {
        setAuthenticated(true);
        return true;
      } else {
        setAuthenticated(false);
        return false;
      }
    } catch (error) {
      console.error('Error during login:', error);
      return false;
    }
  };

  // Function to perform logout
  const logout = () => {
    // Add any cleanup logic for logout
    setAuthenticated(false);
  };

  // Provide the context values to the components
  const contextValue = {
    isAuthenticated,
    login,
    logout,
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
};
