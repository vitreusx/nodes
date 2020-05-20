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
import Error from './Error';
import { ContextMenu, MenuItem, ContextMenuTrigger, connectMenu } from 'react-contextmenu';

const MemberContextMenu = (props) => {
  const { id, trigger } = props;
  const ctx = useContext(AppContext);
  const group = trigger && trigger.data.group;
  const member = trigger && trigger.data.member;
  let exn = null;
  const [showError, setShowError] = useState(false);

  const kick = async () => {
    try {
      console.log(`http://${ctx.addr[0]}/net/g/${group}/m/${member}`);
      await fetch(`http://${ctx.addr[0]}/net/g/${group}/m/${member}`, {
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
      <MenuItem onClick={kick}>
        Kick member out
      </MenuItem>
      <Error show={showError} setShow={setShowError} e={exn} />
    </ContextMenu>
  )
}

const AllMembersContextMenu = (props) => {
  const ctx = useContext(AppContext);
  const [showAdd, setShowAdd] = useState(false);
  const [name, setName] = useState('');
  const [addr, setAddr] = useState('');
  const hideModal = () => setShowAdd(false);
  let exn = null;
  const [showError, setShowError] = useState(false);

  const add = async e => {
    setShowAdd(false);
    try {
      await fetch(`http://${ctx.addr[0]}/net/g/${props.group}/m/${name}?addr=${addr}`, {
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
      <MenuItem onClick={() => setShowAdd(true)}>
        Add a member
      </MenuItem>
      <Modal show={showAdd} onHide={hideModal}>
        <Modal.Header closeButton>
          Add a member
        </Modal.Header>
        <Modal.Body>
          <InputGroup>
            <InputGroup.Prepend>
              <InputGroup.Text>Name</InputGroup.Text>
            </InputGroup.Prepend>
            <FormControl placeholder='Member name' 
            value={name} onChange={e => setName(e.target.value)}/>
          </InputGroup>
          <InputGroup>
            <InputGroup.Prepend>
              <InputGroup.Text>Address</InputGroup.Text>
            </InputGroup.Prepend>
            <FormControl placeholder='Address' 
            value={addr} onChange={e => setAddr(e.target.value)}/>
          </InputGroup>
        </Modal.Body>
        <Modal.Footer>
          <Button variant='outline-secondary' onClick={hideModal}>Cancel</Button>
          <Button variant='outline-primary' onClick={add}>Add</Button>
        </Modal.Footer>
      </Modal>
      <Error show={showError} setShow={setShowError} e={exn} />
    </ContextMenu>
  )
}

const Members = (props) => {
  const ctx = useContext(AppContext);
  const [members, setMembers] = useState([]);

  useEffect(() => {
    const retrieveMembers = async () => {
      if (ctx.addr[0] === null) {
        setMembers([]);
      }
      else {
        try {
          const res = await fetch(`http://${ctx.addr[0]}/net/g/${props.group}`);
          const data = await res.json();
          setMembers(Object.entries(data));
        }
        catch (e) {
          setMembers([]);
        }
      }
    }

    retrieveMembers();
  }, [ctx.addr, ctx.refresh, props.group]);

  const id1 = Math.random().toString();
  const ConnMemberContextMenu = connectMenu(id1)(MemberContextMenu);
  
  const id2 = Math.random().toString();

  return (
    <Tab.Container>
      <Row>
        <Col sm={12}>
          <ContextMenuTrigger id={id2}>
            <Nav variant='pills' className='flex-column vh-100'>
              {members.map(([name, addr], idx) => (
                <ContextMenuTrigger id={id1} data={{ 
                  group: props.group,
                  member: name
                }} collect={props => props}>
                  <Nav.Item>
                    <Nav.Link eventKey={name}>
                      <strong>{name}</strong> ({addr})
                    </Nav.Link>
                  </Nav.Item>
                </ContextMenuTrigger>
              ))}
              <ConnMemberContextMenu />
            </Nav>
          </ContextMenuTrigger>
          <AllMembersContextMenu group={props.group} data={{id: id2}}/>
        </Col>
      </Row>``
    </Tab.Container>
  )
}

export default Members;
