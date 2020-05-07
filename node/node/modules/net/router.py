from flask import Blueprint, request as req
import json
import requests
import socket
import shelve

class Router:
    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip

    def propagate(self, grp):
        for name, addr in grp['members'].items():
            if name != grp['local']:
                yield name, addr

    def __init__(self, conf, port, db):
        self.router = Blueprint('net', __name__)        
        addr = f'{self.get_ip()}:{port}'

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

        @self.router.route('/notify/<group>', methods = ['DELETE'])
        def notify_delete_group(group):
            del db[group]
            return ''

        @self.router.route('/g/<group>', methods = ['DELETE'])
        def delete_group(group):
            if group not in db:
                return 'No such group exists.', 500
            
            for _, addr in self.propagate(db[group]):
                requests.delete(f'http://{addr}/notify/{group}')
            notify_delete_group(group)

            return ''
        
        @self.router.route('/g/<group>/list', methods = ['GET'])
        def list_members(group):
            if group not in db:
                return 'No such group exists.', 500

            return json.dumps(db[group]['members'])

        @self.router.route('/g/<group>/local', methods = ['GET'])
        def get_local_name(group):
            if group not in db:
                return 'No such group exists.', 500
            
            return db[group]['local']
        
        @self.router.route('/notify/<group>/added', methods = ['POST'])
        def notify_added(group):
            if group in db:
                return 'Node is already in such a group.'
            
            db[group] = req.json()
        
        @self.router.route('/notify/<group>/m/<member>', methods = ['PUT'])
        def notify_add_member(group, member):
            db[group]['members'][member] = req.json()['addr']
            return ''

        @self.router.route('/g/<group>/m/<member>', methods = ['PUT'])
        def add_member(group, member):
            if group not in db:
                return 'No such group exists.', 500
            
            grp = db[group]
            if member in grp['members']:
                return 'Member already exists.', 500
            
            payload = req.json()
            requests.post(f'http://{payload["addr"]}/notify/{group}/added', json={
                'local': member,
                'members': grp['members']
            })
            
            for _, addr in self.propagate(grp):
                requests.put(f'http://{addr}/notify/{group}/m/{member}', json=payload)
            notify_add_member(group, member)
            
            return ''

        @self.router.route('/notify/<group>/m/<member>', methods = ['DELETE'])
        def notify_delete_member(group, member):
            del db[group]['members'][member]

        @self.router.route('/g/<group>/m/<member>', methods = ['DELETE'])
        def delete_member(group, member):
            if group not in db:
                return 'No such group exists.', 500
            
            grp = db[group]
            if member not in grp['members']:
                return 'No such member exists.', 500
            
            for _, addr in self.propagate(grp):
                requests.delete(f'http://{addr}/notify/{group}/m/{member}?local')
            notify_delete_member(group, member)

            if member == grp['local']:
                del db[group]
            else:
                requests.delete(f'http://{grp["members"][member]}/notify/{group}')
            
            return ''

        @self.router.route('/g/<group>/leave', methods = ['POST'])
        def leave_group(group):
            if group not in db:
                return 'No such group exists.', 500

            return delete_member(group, db[group]['local'])
            