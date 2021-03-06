import React, { useContext } from 'react';
import { Switch, Route, Link, useLocation } from 'react-router-dom';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import Row from 'react-bootstrap/Row';
import { Helmet } from 'react-helmet';
import Index from './Index';
import General from './General';
import Network from './Network';
import Voice from './Voice';
import Auth from './Auth';
import AppContext from './AppContext';
import './App.css';

const labels = {
  '/': 'Index',
  '/general': 'General',
  '/network': 'Network',
  '/voice': 'Voice',
  '/auth': 'Authorization'
};

const Top = (props) => {
  return (
    <Navbar fixed='top' bg='dark' variant='dark' className='flex-md-nowrap p-0 shadow'>
      <Navbar.Brand className='mr-0 col-sm-3 col-md-2'>
        <Link to='/'><strong>{props.name}</strong></Link>
      </Navbar.Brand>
      <Navbar.Brand className='px-3 w-100 bg-dark'>
        <Nav.Item>{props.current}</Nav.Item>
      </Navbar.Brand>
    </Navbar>
  )
}

const SideItem = (props) => {
  let classIfActive = useLocation().pathname === props.route ? 'active' : '';

  return (
    <Nav.Item key={props.route}>
      <Link className={`nav-link ${classIfActive}`} to={props.route}>
        {labels[props.route]}
      </Link>
    </Nav.Item>
  )
}

const Side = (props) => {
  return (
    <Nav className='col-md-2 d-md-block bg-light sidebar'>
      <div className='sidebar-sticky'>
        <ul className='nav flex-column'>
          {props.routes.map(route => <SideItem route={route} />)}
        </ul>
      </div>
    </Nav>
  )
}

const Content = () => {
  return (
    <main className='col-md-10 ml-sm-auto col-lg-10 px-4' role='main'>
      <Switch>
        <Route path='/general' component={General} />
        <Route path='/network' component={Network} />
        <Route path='/voice' component={Voice} />
        <Route path='/auth' component={Auth} />
        <Route path='/' component={Index} />
      </Switch>
    </main>
  );
}

const App = () => {
  const sidebarRoutes = ['/general', '/network', '/voice', '/auth'];
  const ctx = useContext(AppContext);
  const [addr,] = ctx.addr;

  return (
    <div className='App'>
      <Helmet>
        <title>NC ({addr || 'N/A'})</title>
      </Helmet>
      <Top name='Aurora' current={labels[useLocation().pathname]}/>
      <Container fluid>
        <Row>
          <Side routes={sidebarRoutes}/>
          <Content />
        </Row>
      </Container>
    </div>
  );
}

export default App;
