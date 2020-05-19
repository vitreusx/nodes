from typing import List
import shelve
from os import makedirs
from os.path import dirname
from ..nexus import Nexus
from .config import Config

class Phrases:
    def __init__(self, conf):
        makedirs(dirname(conf.store), exist_ok=True)
        self.db = shelve.open(conf.store, writeback=True)

    def phrases(self) -> List[str]:
        return list(self.db.keys())

    def phrase(self, phrase):
        return self.db.get(phrase)
    
    def create(self, phrase, endpoint, payload):
        if phrase in self.db:
            return
        
        self.db[phrase] = {
            'endpoint': endpoint,
            'payload': payload
        }
        return self.db[phrase]

    def remove(self, phrase):
        if phrase not in self.db:
            return False
        
        del self.db[phrase]
        return True
