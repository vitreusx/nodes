import React, { useContext, useState, useEffect } from 'react';
import Nav from 'react-bootstrap/Nav';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Modal from 'react-bootstrap/Modal';
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import Button from 'react-bootstrap/Button';
import ToggleButton from 'react-bootstrap/ToggleButton';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import AppContext from './AppContext';
import Form from 'react-bootstrap/Form';
import { ContextMenu, MenuItem, ContextMenuTrigger, connectMenu } from 'react-contextmenu';
import './ContextMenu.scss';
import './Voice.css';

const PhraseContextMenu = (props) => {
  const { id, trigger } = props;
  const ctx = useContext(AppContext);
  const phrase = trigger && trigger.data.phrase;

  const remove = async () => {
    try {
      await fetch(`https://${ctx.addr[0]}/voice/p/${phrase}`, { 
        method: 'DELETE',
        headers: {
          'Authorization': 'Basic ' + btoa(ctx.login[0] + ':' + ctx.pass[0])
        }
      });
      ctx.voiceRefr[1](ctx.voiceRefr[0] + 1);
    }
    catch (e) {}
  }

  return (
    <ContextMenu id={id}>
      <MenuItem onClick={remove}>
        Remove the phrase bind
      </MenuItem>
    </ContextMenu>
  )
}

const PhrasesPanContextMenu = (props) => {
  const ctx = useContext(AppContext);
  const [showCreate, setShowCreate] = useState(false);
  const [phrase, setPhrase] = useState('');
  const hideModal = () => setShowCreate(false);

  const create = async e => {
    setShowCreate(false);
    try {
      await fetch(`https://${ctx.addr[0]}/voice/p/${phrase}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Basic ' + btoa(ctx.login[0] + ':' + ctx.pass[0])
        },
        body: JSON.stringify({
          'endpoint': '',
          'payload': {}
        })
      });
      ctx.voiceRefr[1](ctx.voiceRefr[0] + 1);
    }
    catch (e) {}
  }

  return (
    <ContextMenu id={props.data.id}>
      <MenuItem onClick={() => setShowCreate(true)}>
        Create a phrase bind
      </MenuItem>
      <Modal show={showCreate} onHide={hideModal}>
        <Modal.Header closeButton>
          Create a phrase bind
        </Modal.Header>
        <Modal.Body>
          <InputGroup>
            <InputGroup.Prepend>
              <InputGroup.Text>Phrase</InputGroup.Text>
            </InputGroup.Prepend>
            <FormControl placeholder='Phrase' 
            value={phrase} onChange={e => setPhrase(e.target.value)}/>
          </InputGroup>
        </Modal.Body>
        <Modal.Footer>
          <Button variant='outline-secondary' onClick={hideModal}>Cancel</Button>
          <Button variant='outline-primary' onClick={create}>Create</Button>
        </Modal.Footer>
      </Modal>
    </ContextMenu>
  )
}

const Phrases = () => {
  const ctx = useContext(AppContext);
  const [phrases, setPhrases] = useState([]);
  const [phrase, setPhrase] = useState('');
  const [endpoint, setEndpoint] = useState('');
  const [payload, setPayload] = useState('');

  useEffect(() => {
    const retrievePhrases = async () => {
      if (ctx.addr[0] === null) {
        setPhrases([]);
      }
      else {
        try {
          const res = await fetch(`https://${ctx.addr[0]}/voice/phrases`, {
            headers: {
              'Authorization': 'Basic ' + btoa(ctx.login[0] + ':' + ctx.pass[0])
            }
          });
          const data = await res.json();
          setPhrases(data);
        }
        catch (e) {
          setPhrases([]);
        }
      }
    };

    retrievePhrases();
  }, [ctx.addr, ctx.voiceRefr, ctx.login, ctx.pass]);

  const id1 = Math.random().toString();
  const id2 = Math.random().toString();
  const ConnPhraseContextMenu = connectMenu(id2)(PhraseContextMenu);

  const selectPhrase = async (key, ev) => {
    if (ctx.addr[0] === null) {
      setPhrase('');
      setEndpoint('');
      setPayload('');
    }
    else {
      try {
        const res = await fetch(`https://${ctx.addr[0]}/voice/p/${key}`, {
          headers: {
            'Authorization': 'Basic ' + btoa(ctx.login[0] + ':' + ctx.pass[0])
          }
        });
        const data = await res.json();
        setPhrase(key);
        setEndpoint(data['endpoint']);
        setPayload(JSON.stringify(data['payload']));
      }
      catch (e) {
        setPhrase('');
        setEndpoint('');
        setPayload('');
      }
    }
  }

  const updateBind = async () => {
    if (ctx.addr[0] !== null) {
      try {
        await fetch(`https://${ctx.addr[0]}/voice/p/${phrase}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + btoa(ctx.login[0] + ':' + ctx.pass[0])
          },
          body: JSON.stringify({
            'endpoint': endpoint,
            'payload': JSON.parse(payload)
          })
        });
        ctx.voiceRefr[1](ctx.voiceRefr[0] + 1);
      }
      catch (e) {}
    }
  }

  return (
    <Row>
      <Col sm={3} className='border'>
        <ContextMenuTrigger id={id1}>
          <Nav variant='pills' className='flex-column vh-100'>
            {phrases.map(phrase => (
              <ContextMenuTrigger id={id2} data={{phrase: phrase}} collect={props => props}>
                <Nav.Item>
                  <Nav.Link eventKey={phrase} onSelect={selectPhrase}>
                    <strong>{phrase}</strong>
                  </Nav.Link>
                </Nav.Item>
              </ContextMenuTrigger>
            ))}
            <ConnPhraseContextMenu />
          </Nav>
        </ContextMenuTrigger>
        <PhrasesPanContextMenu data={{id: id1}} />
      </Col>
      <Col sm={9}>
        <Form>
          <Form.Group controlId='phrase.endpoint'>
            <Form.Label>Endpoint</Form.Label>
            <Form.Control type='text' placeholder='Endpoint' 
              value={endpoint} onChange={e => setEndpoint(e.target.value)} />
          </Form.Group>
          <Form.Group controlId='phrase.payload'>
            <Form.Label>Payload</Form.Label>
            <Form.Control as='textarea' className='payload-area' 
              value={payload} onChange={e => setPayload(e.target.value)} />
          </Form.Group>
          <div class='text-right'>
            <Button variant='outline-primary' onClick={updateBind}>
              Update the phrase bind
            </Button>
          </div>
        </Form>
      </Col>
    </Row>    
  )
}

const Voice = () => {
  const ctx = useContext(AppContext);
  const [enabled, setEnabled] = useState(null);

  useEffect(() => {
    const retrieveEnabled = async () => {
      if (ctx.addr[0] === null) {
        setEnabled(null);
      }
      else {
        try {
          const res = await fetch(`https://${ctx.addr[0]}/voice`, {
            headers: {
              'Authorization': 'Basic ' + btoa(ctx.login[0] + ':' + ctx.pass[0])
            }
          });
          const data = await res.text();
          setEnabled(data === 'True');
        }
        catch (e) {
          setEnabled(null);
        }
      }
    }

    retrieveEnabled();
  }, [ctx.addr, ctx.login, ctx.pass]);

  const toggleVoice = async () => {
    try {
      await fetch(`https://${ctx.addr[0]}/voice`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Basic ' + btoa(ctx.login[0] + ':' + ctx.pass[0])
        },
        body: JSON.stringify({
          'state': !enabled
        })
      });
      setEnabled(!enabled);
    }
    catch (e) {
      setEnabled(null);
    }
  };

  return (
    <Container fluid>
      <Row className='mt-3 mb-3'>
      <ButtonGroup toggle>
        <ToggleButton type='checkbox' variant='outline-primary' checked={enabled === true} onClick={toggleVoice}>
          {enabled === true ? 'Voice enabled': 'Voice disabled'}
        </ToggleButton>
      </ButtonGroup>
      </Row>
      <Phrases />
    </Container>
  )
}

export default Voice;