import React, { useContext, useState } from 'react';
import PropTypes from 'prop-types';
import Nav from 'react-bootstrap/Nav';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Tab from 'react-bootstrap/Tab';
import Modal from 'react-bootstrap/Modal';
import AppContext from './AppContext';
import Members from './Members';

import { ContextMenu, MenuItem, ContextMenuTrigger, connectMenu } from 'react-contextmenu';

const GroupContextMenu = (props) => {
  const { id, trigger } = props;
  const ctx = useContext(AppContext);
  const group = trigger && trigger.data.group;
  let exn = null;
  const [showError, setShowError] = useState(false);

  const leave = async e => {
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

  const destroy = async e => {
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
      <Modal show={showError} onHide={() => setShowError(false)} animation={false}>
        <Modal.Header closeButton>
          An error occured!
        </Modal.Header>
        <Modal.Body>
          Server response: {exn && exn.toString()}
        </Modal.Body>
      </Modal>
    </ContextMenu>
  )
}

GroupContextMenu.propTypes = {
  id: PropTypes.string.isRequired,
  trigger: PropTypes.shape({
      name: PropTypes.string.isRequired,
      onItemClick: PropTypes.func.isRequired,
      allowRemoval: PropTypes.bool
  }).isRequired
};

const ConnGroupContextMenu = connectMenu('group-ctx')(GroupContextMenu);

const AllGroupsContextMenu = () => {
  return (
    <ContextMenu id='all-groups-ctx'>
      <MenuItem>
        Create a group
      </MenuItem>
    </ContextMenu>
  )
}

const Groups = () => {
  const ctx = useContext(AppContext);
  return (
    <Tab.Container>
      <Row>
        <Col sm={4}>
          <ContextMenuTrigger id='all-groups-ctx'>
            <Nav variant='pills' className='flex-column vh-100'>
              {(ctx.groups || []).map(group => (
                <ContextMenuTrigger id='group-ctx' data={{ group: group }} 
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
          <AllGroupsContextMenu />
        </Col>
        <Col sm={8}>
          <Tab.Content>
            {(ctx.groups || []).map(group => (
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