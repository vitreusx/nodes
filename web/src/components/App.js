import React from 'react';
import { Switch, Route, Link, useLocation } from 'react-router-dom';
import Index from './Index';
import General from './General';
import Network from './Network';
import Voice from './Voice';
import Features from './Features';
import './App.css';

const App = () => {
  const labels = {
    '/': 'Index',
    '/general': 'General',
    '/network': 'Network',
    '/voice': 'Voice',
    '/features': 'Features'
  };

  const Navbar = () => {
    return (
      <nav className='navbar navbar-dark fixed-top bg-dark flex-md-nowrap p-0 shadow'>
        <Link className='navbar-brand col-sm-3 col-md-2 mr-0' to='/'>
          <strong>Aurora</strong> 
        </Link>
        <div className='navbar-brand bg-dark px-3 w-100'>
          <span className='nav-item'>{labels[useLocation().pathname]}</span>
        </div>
      </nav>
    );
  }

  const Sidebar = () => {
    const sidebarRoutes = ['/general', '/network', '/voice', '/features'];

    const Item = (props) => {
      let activeClass = useLocation().pathname === props.route ? 'active' : '';
      
      return (
        <li className='nav-item' key={props.route}>
          <Link className={`nav-link ${activeClass}`} to={props.route}>
            {labels[props.route]}
          </Link>
        </li>
      )
    }

    const items = sidebarRoutes.map((route) =>
      <Item route={route} />
    );

    return (
      <nav className='col-md-2 d-md-block bg-light sidebar'>
        <div className='sidebar-sticky'>
          <ul className='nav flex-column'>
            {items}
          </ul>
        </div>
      </nav>
    );
  }

  const Primary = () => {
    return (
      <main className='col-md-9 ml-sm-auto col-lg-10 px-4' role='main'>
        <Switch>
          <Route path='/general' component={General} />
          <Route path='/network' component={Network} />
          <Route path='/voice' component={Voice} />
          <Route path='/features' component={Features} />
          <Route path='/' component={Index} />
        </Switch>
      </main>
    );
  }

  return (
    <div className='App'>
      <Navbar />
      <div className='container-fluid'>
        <div className='row'>
          <Sidebar />
          <Primary />
        </div>
      </div>
    </div>
  );
}

export default App;
