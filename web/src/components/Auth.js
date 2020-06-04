import React, { useContext, useState, useEffect } from 'react';
import Button from 'react-bootstrap/Button';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Nav from 'react-bootstrap/Nav';
import AppContext from './AppContext';
import Modal from 'react-bootstrap/Modal';
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import { ContextMenu, MenuItem, ContextMenuTrigger, connectMenu } from 'react-contextmenu';

const AcceptContextMenu = (props) => {
  const {id, trigger} = props;
  const ctx = useContext(AppContext);
  const hash = trigger && trigger.data.hash;

  const accept = async e => {
    try {
      await fetch(`https://${ctx.addr[0]}/connect/accept`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Basic ' + btoa(ctx.login[0] + ':' + ctx.pass[0])
        },
        body: JSON.stringify({
          'hash': hash,
        })
      });
      ctx.authRefr[1](ctx.authRefr[0] + 1);
    }
    catch (e) {}
  }
  
  return (
    <ContextMenu id={id}>
      <MenuItem onClick={accept}>
        Accept a pending connection
      </MenuItem>
    </ContextMenu>
  )
}

const StartContextMenu = (props) => {
  const ctx = useContext(AppContext);
  const [showStart, setShowStart] = useState(false);
  const [name, setName] = useState('');
  const [addr, setAddr] = useState('');
  const hideModal = () => setShowStart(false);

  const start = async e => {
    setShowStart(false);
    try {
      await fetch(`https://${ctx.addr[0]}/connect/start`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Basic ' + btoa(ctx.login[0] + ':' + ctx.pass[0])
        },
        body: JSON.stringify({
          'name': name,
          'address': addr
        })
      });
      ctx.authRefr[1](ctx.authRefr[0] + 1);
    }
    catch (e) {}
  }

  return (
    <ContextMenu id={props.data.id}>
      <MenuItem onClick={() => setShowStart(true)}>
        Start a handshake
      </MenuItem>
      <Modal show={showStart} onHide={hideModal}>
        <Modal.Header closeButton>
          Start a handshake
        </Modal.Header>
        <Modal.Body>
          <InputGroup>
            <InputGroup.Prepend>
              <InputGroup.Text>Node Name</InputGroup.Text>
            </InputGroup.Prepend>
            <FormControl placeholder='Node Name' value={name} onChange={e => setName(e.target.value)} />
          </InputGroup>
          <InputGroup>
            <InputGroup.Prepend>
              <InputGroup.Text>Node Address</InputGroup.Text>
            </InputGroup.Prepend>
            <FormControl placeholder='Node Address' value={name} onChange={e => setAddr(e.target.value)} />
          </InputGroup>
        </Modal.Body>
        <Modal.Footer>
          <Button variant='outline-secondary' onClick={hideModal}>Cancel</Button>
          <Button variant='outline-primary' onClick={start}>Start</Button>
        </Modal.Footer>
      </Modal>
    </ContextMenu>
  )
}

const Auth = () => {
  const ctx = useContext(AppContext);
  const [pending, setPending] = useState([]);
  const [accepted, setAccepted] = useState([]);

  const id1 = Math.random().toString();
  const id2 = Math.random().toString();
  const ConnAcceptMenu = connectMenu(id2)(AcceptContextMenu);

  useEffect(() => {
    const retrievePending = async () => {
      if (ctx.addr[0] === null) {
        setPending([]);
      }
      else {
        try {
          const res = await fetch(`https://${ctx.addr[0]}/connect/pending`, {
            headers: {
              'Authorization': 'Basic ' + btoa(ctx.login[0] + ':' + ctx.pass[0])
            }
          });
          const data = await res.json();
          setPending(data["conns"]);
        }
        catch (e) {
          setPending([]);
        }
      }
    }

    retrievePending();
  }, [ctx.addr, ctx.refresh, ctx.authRefr, ctx.login, ctx.pass]);

  useEffect(() => {
    const retrieveAccepted = async () => {
      if (ctx.addr[0] === null) {
        setAccepted([]);
      }
      else {
        try {
          const res = await fetch(`https://${ctx.addr[0]}/connect/accepted`, {
            headers: {
              'Authorization': 'Basic ' + btoa(ctx.login[0] + ':' + ctx.pass[0])
            }
          });
          const data = await res.json();
          setAccepted(data);
        }
        catch (e) {
          setAccepted([]);
        }
      }
    }

    retrieveAccepted();
  }, [ctx.addr, ctx.refresh, ctx.authRefr, ctx.login, ctx.pass]);

  const refr = () => {
    ctx.authRefr[1](ctx.authRefr[0] + 1);
  }

  return (
    <Container>
      <Row className='justify-content-center'>
        <ButtonGroup className='mt-3 mb-3'>
          <Button className='mr-3' variant='outline-primary' onClick={refr}>Refresh</Button>
        </ButtonGroup>
      </Row>
      <Row className='justify-content-around'>
        <Col sm={1}></Col>
        <Col sm={4} className='border'>
          <ContextMenuTrigger id={id1}>
            <Nav variant='pills' className='flex-column vh-100'>
              {pending.map(pend => (
                <ContextMenuTrigger id={id2} data={{ hash: pend['hash'] }} collect={props => props}>
                  <Nav.Item>
                    <Nav.Link>
                      <strong>{pend['nodeName']}</strong>
                      ({pend['hash'].substring(0, 8)}...)
                    </Nav.Link>
                  </Nav.Item>
                </ContextMenuTrigger>
              ))}
              <ConnAcceptMenu />
            </Nav>
          </ContextMenuTrigger>
          <StartContextMenu data={{id: id1}} />
        </Col>
        <Col sm={4} className='border'>
          <Nav variant='pills' className='flex-column vh-100'>
            {accepted.map(accp => (
              <Nav.Item>
                <Nav.Link>
                  {accp}
                </Nav.Link>
              </Nav.Item>
            ))}
          </Nav>
        </Col>
        <Col sm={1}></Col>
      </Row>
    </Container>
  )
}

export default Auth;
