import React, { useContext } from 'react';
import AppContext from './AppContext';

const Network = () => {
  const [addr, setAddr] = useContext(AppContext).addr;
  return <h2>{addr}</h2>;
}

export default Network;