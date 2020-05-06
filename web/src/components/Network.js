import React, { useContext, useState, useEffect } from 'react';
import AppContext from './AppContext';
import './Network.css';

const Network = () => {
  const ctx = useContext(AppContext);
  const addr = ctx.addr[0];
  const groups = ctx.groups;

  const [selected, setSelected] = useState(null);
  const [members, setMembers] = useState(null);

  const GroupRow = (props) => {
    const changeSelection = e => {
      setSelected(selected === props.group ? null : props.group);
    }
    return (
      <tr data-name={props.group} onClick={changeSelection} 
      className={`group-row ${selected === props.group ? 'selected' : ''}`}>
        <td>{props.group}</td>
      </tr>
    )
  }

  const GroupsTable = () => {
    return (
      <table className='table table-hover'>
        <thead className='thead-dark'>
          <tr>
            <th>Groups</th>
          </tr>
        </thead>
        <tbody>
          {(groups || []).map(group => <GroupRow key={group} group={group} />)}
        </tbody>
      </table>
    );
  }

  useEffect(() => {
    const retrieveMembers = async () => {
      try {
        const res = await fetch(`http://${addr}/net/g/${selected}/list`);
        const data = await res.json();
        setMembers(data);
      }
      catch (e) {
        setMembers(null);
      }
    }

    retrieveMembers();
  }, [addr, selected]);

  const MemberRow = (props) => {
    return (
      <tr data-name={props.name}>
        <td>{props.addr}</td>
        <td>{props.name}</td>
      </tr>
    )
  }

  const MembersTable = () => {
    return (
      <table className='table table-hover'>
        <thead className='thead-dark'>
          <tr>
            <th colSpan={2}>Members</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(members || {})
            .map(([name, addr], idx) => 
              <MemberRow key={name} name={name} addr={addr}/>)}
        </tbody>
      </table>
    );
  }

  return (
    <div className='container-fluid mt-3'>
      <div className='row'>
        <div className='col-md-2 table-responsive'>
          <GroupsTable />
        </div>
        <div className='col-md-2 table-responsive'>
          <MembersTable />
        </div>
      </div>
    </div>
  )
}

export default Network;