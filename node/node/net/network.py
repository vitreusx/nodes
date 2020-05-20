from typing import List, Dict
import shelve
from os import makedirs
from os.path import dirname
from .config import Config

class Group:
    def __init__(self, group):
        self.group = group

    def members(self) -> Dict[str, str]:
        return self.group['members']
        
    def member(self, alias):
        return self.group['members'].get(alias)

    def invite(self, alias, addr):
        if alias in self.group['members']:
            return False
        self.group['members'][alias] = addr
        return True

    def kick(self, alias):
        if alias not in self.group['members']:
            return False
        
        del self.group['members'][alias]
        return True

class Network:
    def __init__(self, conf):
        self.conf = conf
        makedirs(dirname(conf.store), exist_ok=True)
        self.db = shelve.open(conf.store, writeback=True)

    def groups(self) -> List[str]:
        return list(self.db.keys())

    def group(self, group) -> Group:
        if group in self.db:
            return Group(self.db[group])
    
    def create(self, group) -> Group:
        if group in self.db:
            return
        
        self.db[group] = {
            'local': self.conf.name,
            'members': {
                self.conf.name: self.conf.addr
            }
        }
        return self.group(group)

    def erase(self, group):
        if group not in self.db:
            return False
        
        del self.db[group]
        return True
