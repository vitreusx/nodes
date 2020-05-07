import React, { useContext } from 'react';
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import AppContext from './AppContext';

const General = () => {
  const ctx = useContext(AppContext);
  const [addr, setAddr] = ctx.addr;

  return (
    <div>
      <InputGroup className='mb-3 mt-3'>
        <InputGroup.Prepend>
          <InputGroup.Text>Node address</InputGroup.Text>
        </InputGroup.Prepend>
        <FormControl placeholder='Address/Hostname' 
        value={addr} onChange={e => setAddr(e.target.value)} />
      </InputGroup>
    </div>
  )
}

export default General;
