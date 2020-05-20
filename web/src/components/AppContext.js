import React, { useState } from 'react';

const AppContext = React.createContext();

export const AppProvider = ({ children }) => {
  const [addr, setAddr] = useState(null);
  const [refresh, setRefresh] = useState(0);

  const state = {
    addr: [addr, setAddr],
    refresh: [refresh, setRefresh]
  }

  return (
    <AppContext.Provider value={state}>
      {children}
    </AppContext.Provider>
  );
}

export default AppContext;