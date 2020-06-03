from ..nexus import Nexus
from .config import Config
from .network import Network
from .authorization import Authorization
from flask import request as req, abort, url_for
from flask_restful import Resource
import requests
import json

class Installer:
    def __init__(self, nx: Nexus):
        conf = Config(nx.conf.get('net') or {})
        network = Network(conf)

        @nx.httpauth.verify_password
        def verify(username, password):
            return nx.auth.validate_user(username, password)

        class Groups(Resource):
            @nx.httpauth.login_required
            def get(self):
                return network.groups()
                
        nx.api.add_resource(Groups, '/net/groups', endpoint='api.groups')
        
        def fetch_group(group):
            rv = network.group(group)
            if not rv:
                abort(404, f'Group {group} does not exist.')
            return rv

        class Group(Resource):
            @nx.httpauth.login_required
            def get(self, group):
                return fetch_group(group).members()
            
            @nx.httpauth.login_required
            def put(self, group):
                if not network.create(group):
                    return False
                fetch_group(group).invite(conf['net']['name'], conf.addr)
                return True
            
            @nx.httpauth.login_required
            def delete(self, group):
                if 'local' not in req.args:
                    mems = dict(fetch_group(group).members())
                    for mem in mems:
                        ur = url_for('api.group', group=group, local=True)
                        other_node_name = mem
                        requests.delete(f'https://{mems[mem]}{ur}',
                                        **nx.auth.get_requests_auth(other_node_name))

                return network.erase(group)

        nx.api.add_resource(Group, '/net/g/<group>', endpoint='api.group')
        
        # Private
        @nx.app.route('/net/sync/join', methods=['POST'])
        @nx.httpauth.login_required
        def join():
            network.db[req.json['group']] = {
                'local': req.json['local'],
                'members': req.json['members']
            }
            return ''

        class Member(Resource):
            @nx.httpauth.login_required
            def get(self, group, member):
                return fetch_group(group).member(member)
            
            @nx.httpauth.login_required
            def put(self, group, member):
                g = fetch_group(group)
                g.invite(member, req.args['addr'])

                mems = dict(g.members())
                if 'local' not in req.args:
                    for mem in mems:
                        if mem != member:
                            other_node_name = mem
                            ur = url_for('api.member',\
                                group=group, member=member,\
                                addr=req.args['addr'], local=True)
                            requests.put(f'https://{mems[mem]}{ur}', **nx.auth.get_requests_auth(other_node_name))

                    other_node_name = mem
                    requests.post(f'https://{req.args["addr"]}/net/sync/join', json={
                        'group': group,
                        'local': member,
                        'members': network.db[group]['members']
                    },
                    **nx.auth.get_requests_auth(other_node_name))
            
            @nx.httpauth.login_required
            def delete(self, group, member):
                g = fetch_group(group)
                mems = dict(g.members())
                if 'local' not in req.args:
                    for mem in mems:
                        other_node_name = mem
                        ur = url_for('api.member',\
                            group=group, member=member, local=True)
                        requests.delete(f'https://{mems[mem]}{ur}',
                        **nx.auth.get_requests_auth(other_node_name))
                if not g.kick(member):
                    return False
                if len(g.members()) == 0 or member == network.db[group]['local']:
                    network.erase(group)
                return True

        nx.api.add_resource(Member, '/net/g/<group>/m/<member>', endpoint='api.member')

        @nx.app.route('/net/g/<group>/leave', methods=['POST'])
        @nx.httpauth.login_required
        def leave(group):
            g = network.db.get(group)
            if not g:
                abort(404, f'Group {group} does not exist.')
            ur = url_for('api.member', group=group, member=g['local'], _external=True)
            other_node_name = g['local'] # ??? I dont understand this code Jakub please fix
            r = requests.delete(ur, **nx.auth.get_requests_auth(other_node_name))
            return r.content, r.status_code

        @nx.app.route('/net/proxy', methods=['POST'])
        @nx.httpauth.login_required
        def proxy():
            targets = []
            for trgt in req.json['targets']:
                if isinstance(trgt, str):
                    targets += [(trgt, mem) for mem in network.group(trgt).members()]
                elif isinstance(trgt, dict):
                    for grp in trgt:
                        targets += [(grp, mem) for mem in trgt[grp]]
            
            for grp, mem in targets:
                url = f'https://{network.group(grp).member(mem)}{req.json["endpoint"]}'
                other_node_name = mem
                requests.post(url, json=req.json['payload'], **nx.auth.get_requests_auth(other_node_name))

        # Adds authorized user on this node
        # Request contains json with username and password fields
        @nx.app.route('/net/adduser', methods=['POST'])
        @nx.httpauth.login_required
        def add_user():
            username = str(req.json['username'])
            password = str(req.json['password'])

            nx.auth.add_user(username, password)
            return ''

        # Someone gives us access token to them
        # Request contains 
        # name - name of node for which this token is for
        # token - access token
        # This means that we have been added as user on this node
        @nx.app.route('/net/addtoken', methods=['POST'])
        @nx.httpauth.login_required
        def add_access_token():
            other_node_name = str(req.json['name'])
            token = str(req.json['name'])

            nx.auth.add_access_token(other_node_name, token)
            return ''
