import React, { useState } from 'react';
import Button from 'react-bootstrap/Button';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import Groups from './Groups';
import './Network.css';
import './ContextMenu.scss';

const Network = () => {
  const [,setDummy] = useState();
  
  return (
    <div>
      <ButtonGroup className='mt-3 mb-3'>
        <Button variant='outline-primary' onClick={() => setDummy({})}>Refresh</Button>
      </ButtonGroup>
      <Groups />
    </div>
  )
}

export default Network;