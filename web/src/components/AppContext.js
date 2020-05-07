import React, { useState, useEffect } from 'react';

const AppContext = React.createContext();

export const AppProvider = ({ children }) => {
  const [addr, setAddr] = useState(null);
  const [groups, setGroups] = useState(null);

  useEffect(() => {
    const retrieveGroups = async () => {
      if (addr === null) {
        setGroups(null);
      }
      else {
        try {
          const res = await fetch(`http://${addr}/net/list`);
          const data = await res.json();
          setGroups(data);
        }
        catch (e) {
          setGroups(null);
        }
      }
    } 

    retrieveGroups();
  }, [addr]);

  const state = {
    addr: [addr, setAddr],
    groups: groups
  }

  return (
    <AppContext.Provider value={state}>
      {children}
    </AppContext.Provider>
  );
}

export default AppContext;