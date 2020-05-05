import React, { useContext } from 'react';
import AppContext from './AppContext';

const General = () => {
  const [addr, setAddr] = useContext(AppContext).addr;

  return (
    <div>
      <div className='input-group mb-3 mt-3'>
        <div className='input-group-prepend'>
          <span className='input-group-text'>Node address</span>
        </div>
        <input type='text' className='form-control' placeholder='Address/Hostname'
               value={addr} onChange={e => setAddr(e.target.value)}/>
      </div>
      <span>{addr}</span>
    </div>
  )
}

export default General;