from ..nexus import Nexus
from .config import Config
from .network import Network
from flask import request as req, abort, url_for
from flask_restful import Resource
import requests
import json

class Installer:
    def __init__(self, nx: Nexus):
        conf = Config(nx.conf.get('net') or {})
        network = Network(conf)

        USER_DATA = {
            "local": "localtoken"
        }

        @nx.auth.verify_password
        def verify(username, password):
            if not (username and password):
                return False
            return USER_DATA.get(username) == password

        class Groups(Resource):
            @nx.auth.login_required
            def get(self):
                return network.groups()
                
        nx.api.add_resource(Groups, '/net/groups', endpoint='api.groups')
        
        def fetch_group(group):
            rv = network.group(group)
            if not rv:
                abort(404, f'Group {group} does not exist.')
            return rv

        class Group(Resource):
            @nx.auth.login_required
            def get(self, group):
                return fetch_group(group).members()
            
            @nx.auth.login_required
            def put(self, group):
                if not network.create(group):
                    return False
                fetch_group(group).invite(conf.name, conf.addr)
                return True
            
            @nx.auth.login_required
            def delete(self, group):
                if 'local' not in req.args:
                    mems = dict(fetch_group(group).members())
                    for mem in mems:
                        ur = url_for('api.group', group=group, local=True)
                        requests.delete(f'http://{mems[mem]}{ur}')
                return network.erase(group)

        nx.api.add_resource(Group, '/net/g/<group>', endpoint='api.group')
        
        @nx.app.route('/net/sync/join', methods=['POST'])
        @nx.auth.login_required
        def join():
            network.db[req.json['group']] = {
                'local': req.json['local'],
                'members': req.json['members']
            }
            return ''

        class Member(Resource):
            @nx.auth.login_required
            def get(self, group, member):
                return fetch_group(group).member(member)
            
            @nx.auth.login_required
            def put(self, group, member):
                g = fetch_group(group)
                g.invite(member, req.args['addr'])

                mems = dict(g.members())
                if 'local' not in req.args:
                    for mem in mems:
                        if mem != member:
                            ur = url_for('api.member',\
                                group=group, member=member,\
                                addr=req.args['addr'], local=True)
                            requests.put(f'http://{mems[mem]}{ur}')
                    requests.post(f'http://{req.args["addr"]}/net/sync/join', json={
                        'group': group,
                        'local': member,
                        'members': network.db[group]['members']
                    })
            
            @nx.auth.login_required
            def delete(self, group, member):
                g = fetch_group(group)
                mems = dict(g.members())
                if 'local' not in req.args:
                    for mem in mems:
                        ur = url_for('api.member',\
                            group=group, member=member, local=True)
                        requests.delete(f'http://{mems[mem]}{ur}')
                if not g.kick(member):
                    return False
                if len(g.members()) == 0 or member == network.db[group]['local']:
                    network.erase(group)
                return True

        nx.api.add_resource(Member, '/net/g/<group>/m/<member>', endpoint='api.member')

        @nx.app.route('/net/g/<group>/leave', methods=['POST'])
        @nx.auth.login_required
        def leave(group):
            g = network.db.get(group)
            if not g:
                abort(404, f'Group {group} does not exist.')
            ur = url_for('api.member', group=group, member=g['local'], _external=True)
            r = requests.delete(ur)
            return r.content, r.status_code

        @nx.app.route('/net/proxy', methods=['POST'])
        @nx.auth.login_required
        def proxy():
            targets = []
            for meta in req.json['targets']:
                if isinstance(meta, str):
                    targets += [(meta, mem) for mem in network.group(meta).members()]
                elif isinstance(meta, dict):
                    for grp in meta:
                        targets += [(grp, mem) for mem in meta[grp]]
            
            for grp, mem in targets:
                url = f'http://{network.group(grp).member(mem)}{req.json["endpoint"]}'
                requests.post(url, json=req.json['payload'])
