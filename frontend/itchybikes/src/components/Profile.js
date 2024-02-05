
import React from 'react';
import { useNavigate } from 'react-router-dom';

const Profile = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    // Clear user's authentication token from localStorage
    localStorage.removeItem('accessToken');

    // Navigate to the home page after logout
    navigate('/home');
  };

  return (
    <div>
      <h2>Profile Page</h2>
      <p>Welcome! You are logged in.</p>
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
};

export default Profile;
