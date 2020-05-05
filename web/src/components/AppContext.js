import React, { useState } from 'react';

const AppContext = React.createContext();

export const AppProvider = ({ children }) => {
  const [addr, setAddr] = useState('');

  const state = {
    addr: [addr, setAddr]
  }

  return (
    <AppContext.Provider value={state}>
      {children}
    </AppContext.Provider>
  );
}

export default AppContext;