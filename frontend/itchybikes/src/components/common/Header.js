// Header Component

import React from 'react';
import { Link } from 'react-router-dom';
import '../../styles/Header.css';

const Header = () => {
  return (
    <header>

    {/* <img src="./logo.jpg" alt="Itchy Bikes" /> */}


      <div className="title">
        <h1>Itchy Bikes</h1>
      </div>
      
      <nav>
        <ul>
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to="/login">Login</Link>
          </li>
          <li>
            <Link to="/signup"><button id='sign-up'>Sign Up</button></Link>
            {/* <Link to="/signup">Sign Up</Link> */}
          </li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;
