from dataclasses import dataclass
import socket

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

@dataclass
class Config:
    store: str = 'db/net.db'
    name: str = '<Node>'
    addr: str = 'localhost:8080'
    port: str = '8080'

    def __init__(self, conf):
        self.__dict__.update(conf or {})
        self.addr = f'{get_ip()}:{conf.get("port") or 8080}'
