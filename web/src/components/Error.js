import React from 'react';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';

const Error = (props) => {
  const hideModal = () => props.setShow(false);

  return (
    <Modal show={props.show} onHide={hideModal}>
      <Modal.Header closeButton>
        <Modal.Title>
          An error occured!
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        Server response: {props.e && props.e.toString()}
      </Modal.Body>
      <Modal.Footer>
        <Button variant='outline-primary' onClick={hideModal}>Return</Button>
      </Modal.Footer>
    </Modal>
  )
}

export default Error;