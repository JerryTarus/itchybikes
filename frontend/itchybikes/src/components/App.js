// App.js
import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Header from './Header/Header';
import Home from './Home/Home';
import Diaries from './Diaries/Diaries';
import Footer from './Footer/Footer';
import Login from './Login/Login';
import SignUp from './Signup/SignUp';

const App = () => {
  return (
    <Router>
      <div className="app">
        <Header />
        <>
          <Route path="/" exact component={Home} />
          <Route path="/diaries" component={Diaries} />
          <Route path="/login" component={Login} />
          <Route path="/signup" component={SignUp} />
        </>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
