import React, { useContext } from 'react';
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import AppContext from './AppContext';

const General = () => {
  const ctx = useContext(AppContext);
  const [addr, setAddr] = ctx.addr;
  const [login, setLogin] = ctx.login;
  const [pass, setPass] = ctx.pass;

  return (
    <div>
      <InputGroup className='mt-3'>
        <InputGroup.Prepend>
          <InputGroup.Text>Node address</InputGroup.Text>
        </InputGroup.Prepend>
        <FormControl placeholder='Address/Hostname' 
        value={addr} onChange={e => setAddr(e.target.value)} />
      </InputGroup>

      <InputGroup className='mt-2'>
        <InputGroup.Prepend>
          <InputGroup.Text>Login</InputGroup.Text>
        </InputGroup.Prepend>
        <FormControl placeholder='Login'
        value={login} onChange={e => setLogin(e.target.value)} />
      </InputGroup>

      <InputGroup className='mt-2'>
        <InputGroup.Prepend>
          <InputGroup.Text>Password</InputGroup.Text>
        </InputGroup.Prepend>
        <FormControl placeholder='Password' type='password'
        value={pass} onChange={e => setPass(e.target.value)} />
      </InputGroup>
    </div>
  )
}

export default General;
