import React, { useContext } from 'react';
import Button from 'react-bootstrap/Button';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Groups from './Groups';
import AppContext from './AppContext';
import './Network.css';
import './ContextMenu.scss';

const Network = () => {
  const ctx = useContext(AppContext);
  const [addr, setAddr] = ctx.addr;

  const refresh = () => {
    setAddr(addr);
    ctx.refresh[1](ctx.refresh[0] + 1);
  }
  
  return (
    <Container fluid>
      <Row className='justify-content-center'>
        <ButtonGroup className='mt-3 mb-3'>
          <Button variant='outline-primary' onClick={refresh}>Refresh</Button>
        </ButtonGroup>
      </Row>
      <Groups />
    </Container>
  )
}

export default Network;