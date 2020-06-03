import React, { useState } from 'react';

const AppContext = React.createContext();

export const AppProvider = ({ children }) => {
  const [addr, setAddr] = useState(null);
  const [refresh, setRefresh] = useState(0);
  const [voiceRefr, setVoiceRefr] = useState(0);
  const [login, setLogin] = useState('');
  const [pass, setPass] = useState('');

  const state = {
    addr: [addr, setAddr],
    refresh: [refresh, setRefresh],
    voiceRefr: [voiceRefr, setVoiceRefr],
    login: [login, setLogin],
    pass: [pass, setPass]
  }

  return (
    <AppContext.Provider value={state}>
      {children}
    </AppContext.Provider>
  );
}

export default AppContext;