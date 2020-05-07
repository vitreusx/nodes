import React, { useContext } from 'react';
import Button from 'react-bootstrap/Button';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import Groups from './Groups';
import './Network.css';
import './ContextMenu.scss';
import AppContext from './AppContext';

const Network = () => {
  const ctx = useContext(AppContext);
  const forceUpdate = () => {
    const [addr, setAddr] = ctx.addr;
    const tmp = JSON.parse(JSON.stringify(addr));
    setAddr(null);
    setAddr(tmp);
  }
  
  return (
    <div>
      <ButtonGroup className='mt-3 mb-3'>
        <Button variant='outline-primary' onClick={forceUpdate}>Refresh</Button>
      </ButtonGroup>
      <Groups />
    </div>
  )
}

export default Network;