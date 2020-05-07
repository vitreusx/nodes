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
import MemberPane from './MemberPane';
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

const ConnMemberContextMenu = connectMenu('member-ctx')(MemberContextMenu);

const AllMembersContextMenu = (props) => {
  const ctx = useContext(AppContext);
  const [showAdd, setShowAdd] = useState(false);
  const [name, setName] = useState();
  const [addr, setAddr] = useState();
  const hideModal = () => setShowAdd(false);
  let exn = null;
  const [showError, setShowError] = useState(false);

  const add = async e => {
    setShowAdd(false);
    try {
      await fetch(`http://${ctx.addr[0]}/net/g/${props.group}/m/${name}`, {
        method: 'PUT',
        body: JSON.stringify({
          addr: addr
        })
      });
    }
    catch (e) {
      exn = e;
      setShowError(true);
    }
  }

  return (
    <ContextMenu id='all-members-ctx'>
      <MenuItem>
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
  const [members, setMembers] = useState(null);

  useEffect(() => {
    const retrieveMembers = async () => {
      if (ctx.addr[0] === null) {
        setMembers(null);
      }
      else {
        try {
          const res = await fetch(`http://${ctx.addr[0]}/net/g/${props.group}/list`);
          const data = await res.json();
          setMembers(Object.entries(data));
        }
        catch (e) {
          setMembers(null);
        }
      }
    }

    retrieveMembers();
  }, [ctx.addr, props.group]);

  return (
    <Tab.Container>
      <Row>
        <Col sm={6}>
          <ContextMenuTrigger id='all-members-ctx'>
            <Nav variant='pills' className='flex-column vh-100'>
              {(members || []).map(([name, addr], idx) => (
                <ContextMenuTrigger id='member-ctx' data={{ 
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
          <AllMembersContextMenu group={props.group}/>
        </Col>
        <Col sm={6}>
          <Tab.Content>
            {(members || []).map(([name, addr], idx) => (
              <Tab.Pane eventKey={name}>
                <MemberPane group={props.group} member={name} />
              </Tab.Pane>
            ))}
          </Tab.Content>
        </Col>
      </Row>``
    </Tab.Container>
  )
}

export default Members;