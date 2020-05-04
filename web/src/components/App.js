import React from 'react';
import './App.css';

class App extends React.Component {
  state = {
    current: 'Index'
  };

  Navbar = (props) => {
    return (
      <nav className='navbar navbar-dark fixed-top bg-dark flex-md-nowrap p-0 shadow'>
        <a className='navbar-brand col-sm-3 col-md-2 mr-0' href='/'>
          <strong> {props.name} </strong>
        </a>
        <div className='navbar-brand bg-dark px-3 w-100'>
          <span className='nav-item'> {props.current} </span>
        </div>
      </nav>
    );
  };

  Primary = (props) => {
    const mods = [
      { label: 'Index', route: '/' },
      { label: 'General', route: '/general' },
      { label: 'Network', route: '/network' },
      { label: 'Voice', route: '/voice' },
      { label: 'Features', route: '/features' }
    ];

    const modItems = mods.map((mod) =>
      <li className='nav-item' key={mod.label}>
        <a className={`nav-link ${this.state.current === mod.label ? 'active' : ''}`} href={mod.route}>
          {mod.label}
        </a>
      </li>
    );

    return (
      <div className='container-fluid'>
        <div className='row'>
          <nav className='col-md-2 d-md-block bg-light sidebar'>
            <div className='sidebar-sticky'>
              <ul className='nav flex-column'>
                {modItems}
              </ul>
            </div>
          </nav>
        </div>
      </div>
    )
  };

  render() {
    return (
      <div className='App'>
        <this.Navbar name='Aurora' current={this.state.current} />
        <this.Primary />        
      </div>
    );
  }
}

export default App;
