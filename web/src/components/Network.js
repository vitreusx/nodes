import React, { useContext } from 'react';
import Button from 'react-bootstrap/Button';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import Groups from './Groups';
import AppContext from './AppContext';
import './Network.css';
import './ContextMenu.scss';

const Network = () => {
  const ctx = useContext(AppContext);
  const [addr, setAddr] = ctx.addr;
  
  return (
    <div>
      <ButtonGroup className='mt-3 mb-3'>
        <Button variant='outline-primary' onClick={() => setAddr(addr)}>Refresh</Button>
      </ButtonGroup>
      <Groups />
    </div>
  )
}

export default Network;