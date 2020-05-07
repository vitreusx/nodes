import React, { useContext, useState, useEffect } from 'react';
import Nav from 'react-bootstrap/Nav';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Tab from 'react-bootstrap/Tab';
import AppContext from './AppContext';
import MemberPane from './MemberPane';

import { ContextMenu, MenuItem, ContextMenuTrigger, connectMenu } from 'react-contextmenu';

const MemberContextMenu = (props) => {
  const { id, trigger } = props;

  return (
    <ContextMenu id={id}>
      <MenuItem>
        Kick member out
      </MenuItem>
    </ContextMenu>
  )
}

const ConnMemberContextMenu = connectMenu('member-ctx')(MemberContextMenu);

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
                <ContextMenuTrigger id='member-ctx' data={{ member: name }}>
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
          <ContextMenu id='all-members-ctx'>
            <MenuItem>
              Add a member
              </MenuItem>
          </ContextMenu>
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