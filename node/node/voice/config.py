from dataclasses import dataclass

@dataclass
class Config:
    enabled: bool = False
    store: str = 'db/voice.db'
    cred: str = 'cred/google.json'
    backend: str = 'google'

    def __init__(self, conf):
        self.__dict__.update(conf.get('voice') or {})
