import React, { useContext } from 'react';
import AppContext from './AppContext';

const General = () => {
  const ctx = useContext(AppContext);
  const [addr, setAddr] = ctx.addr;

  return (
    <div className='input-group mb-3 mt-3'>
      <div className='input-group-prepend'>
        <span className='input-group-text'>Node address</span>
      </div>
      <input type='text' className='form-control' placeholder='Address/Hostname'
        value={addr} onChange={e => setAddr(e.target.value)} />
    </div>
  )
}

export default General;