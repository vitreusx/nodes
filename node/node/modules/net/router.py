from flask import Blueprint, request as req
import json
import requests
import socket
import shelve

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

class Router:
    def __init__(self, conf, port, db):
        self.router = Blueprint('net', __name__)        
        addr = f'{get_ip()}:{port}'

        @self.router.route('/list', methods = ['GET'])
        def list_groups():
            return json.dumps(list(db.keys()))
        
        @self.router.route('/g/<group>', methods = ['PUT'])
        def create_group(group):
            if group in db:
                return 500, 'Group already exists.'
            
            db[group] = {
                'local': conf.get('name'),
                'members': {conf.get('name'): addr}
            }
            return ''

        @self.router.route('/g/<group>', methods = ['DELETE'])
        def delete_group(group):
            if group not in db:
                return 'No such group exists.', 500
            
            grp = db[group]
            if not req.args.get('local'):
                for name, addr in grp['members'].items():
                    if name != grp['local']:
                        requests.delete(f'http://{addr}/g/{group}')

            del db[group]
            return ''
        
        @self.router.route('/g/<group>/list', methods = ['GET'])
        def list_members(group):
            if group not in db:
                return 'No such group exists.', 500

            return json.dumps(db[group]['members'])

        @self.router.route('/g/<group>/m/<member>', methods = ['PUT'])
        def add_member(group, member):
            if group not in db:
                return 'No such group exists.', 500
            
            grp = db[group]
            if member in grp['members']:
                return 'Member already exists.', 500
            
            grp['members'][member] = req.json()['addr']
            return ''

        @self.router.route('/g/<group>/m/<member>', methods = ['DELETE'])
        def delete_member(group, member):
            if group not in db:
                return 'No such group exists.', 500
            
            grp = db[group]
            if member not in grp['members']:
                return 'No such member exists.', 500
            
            if not req.args.get('local'):
                for name, addr in grp['members'].items():
                    if name != grp.local:
                        requests.delete(f'http://{addr}/g/{group}/m/{member}')
            
            del grp[member]
            return ''
