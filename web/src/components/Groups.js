import React, { useContext, useState, useEffect } from 'react';
import Nav from 'react-bootstrap/Nav';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Tab from 'react-bootstrap/Tab';
import Modal from 'react-bootstrap/Modal';
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import Button from 'react-bootstrap/Button';
import AppContext from './AppContext';
import Members from './Members';
import Error from './Error';
import { ContextMenu, MenuItem, ContextMenuTrigger, connectMenu } from 'react-contextmenu';

const GroupContextMenu = (props) => {
  const { id, trigger } = props;
  const ctx = useContext(AppContext);
  const group = trigger && trigger.data.group;
  let exn = null;
  const [showError, setShowError] = useState(false);

  const leave = async () => {
    try {
      await fetch(`http://${ctx.addr[0]}/net/g/${group}/leave`, {
        method: 'POST'
      });
    }
    catch (e) {
      exn = e;
      setShowError(true);
    }
  }

  const destroy = async () => {
    try {
      await fetch(`http://${ctx.addr[0]}/net/g/${group}`, {
        method: 'DELETE'
      });
    }
    catch (e) {
      exn = e;
      setShowError(true);
    }
  }

  return (
    <ContextMenu id={id}>
      <MenuItem onClick={leave}>
        Leave the group
      </MenuItem>
      <MenuItem onClick={destroy}>
        Delete the group
      </MenuItem>
      <Error show={showError} setShow={setShowError} e={exn} />
    </ContextMenu>
  )
}

const AllGroupsContextMenu = (props) => {
  const ctx = useContext(AppContext);
  const [showCreate, setShowCreate] = useState(false);
  const [name, setName] = useState('');
  const hideModal = () => setShowCreate(false);
  let exn = null;
  const [showError, setShowError] = useState(false);

  const create = async e => {
    setShowCreate(false);
    try {
      await fetch(`http://${ctx.addr[0]}/net/g/${name}`, {
        method: 'PUT'
      });
    }
    catch (e) {
      exn = e;
      setShowError(true);
    }
  }

  return (
    <ContextMenu id={props.data.id}>
      <MenuItem onClick={() => setShowCreate(true)}>
        Create a group
      </MenuItem>
      <Modal show={showCreate} onHide={hideModal}>
        <Modal.Header closeButton>
          Create a group
        </Modal.Header>
        <Modal.Body>
          <InputGroup>
            <InputGroup.Prepend>
              <InputGroup.Text>Name</InputGroup.Text>
            </InputGroup.Prepend>
            <FormControl placeholder='Group name' 
            value={name} onChange={e => setName(e.target.value)}/>
          </InputGroup>
        </Modal.Body>
        <Modal.Footer>
          <Button variant='outline-secondary' onClick={hideModal}>Cancel</Button>
          <Button variant='outline-primary' onClick={create}>Create</Button>
        </Modal.Footer>
      </Modal>
      <Error show={showError} setShow={setShowError} e={exn} />
    </ContextMenu>
  )
}

const Groups = () => {
  const ctx = useContext(AppContext);
  const [groups, setGroups] = useState([]);

  useEffect(() => {
    const retrieveGroups = async () => {
      if (ctx.addr[0] === null) {
        setGroups([]);
      }
      else {
        try {
          const res = await fetch(`http://${ctx.addr[0]}/net/groups`);
          const data = await res.json();
          setGroups(data);
        }
        catch (e) {
          setGroups([]);
        }
      }
    }

    retrieveGroups();
  }, [ctx.addr]);

  const id1 = Math.random().toString();
  const id2 = Math.random().toString();
  const ConnGroupContextMenu = connectMenu(id2)(GroupContextMenu);

  return (
    <Tab.Container>
      <Row>
        <Col sm={4}>
          <ContextMenuTrigger id={id1}>
            <Nav variant='pills' className='flex-column vh-100'>
              {groups.map(group => (
                <ContextMenuTrigger id={id2} data={{ group: group }} 
                collect={props => props}>
                  <Nav.Item>
                    <Nav.Link eventKey={group}>
                      <strong>{group}</strong>
                    </Nav.Link>
                  </Nav.Item>
                </ContextMenuTrigger>
              ))}
              <ConnGroupContextMenu />
            </Nav>
          </ContextMenuTrigger>
          <AllGroupsContextMenu data={{id: id1}}/>
        </Col>
        <Col sm={8}>
          <Tab.Content>
            {groups.map(group => (
              <Tab.Pane eventKey={group}>
                <Members group={group} />
              </Tab.Pane>
            ))}
          </Tab.Content>
        </Col>
      </Row>
    </Tab.Container>
  )
}

export default Groups;
