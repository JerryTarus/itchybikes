import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthContext'; 

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const { login } = useAuth(); 
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // Login function from AuthContext
      const success = await login(email, password);

      if (success) {
        setError(null);
        navigate('/Home');
      } else {
        setError('Invalid credentials');
      }
    } catch (error) {
      setError('An unexpected error occurred. Kindly try again.');
      console.error('Error logging in:', error);
    }
  };

  return (
    <div className='login-container'>
      <div className="login-box">
        <h2>Login</h2>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        <form onSubmit={handleSubmit}>
          <label>
            Email:
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
          </label>
          <label>
            Password:
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
          </label>
          <button type="submit">Login</button>
        </form>
      </div>
    </div>
  );
};
export default Login;
