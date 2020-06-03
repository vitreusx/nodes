from ..nexus import Nexus
from .config import Config
from .network import Network
from .authorization import Authorization
from .connecting import ConnectionHandshake
from flask import request as req, abort, url_for
from flask_restful import Resource
import requests
import json


request_method = {
    'get' : requests.get,
    'put' : requests.put,
    'delete' : requests.delete,
    'post' : requests.post,
}


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

            try:
                sender = request_methods[req.json['method']]
            except:
                sender = requests.post
            
            for grp, mem in targets:
                url = f'https://{network.group(grp).member(mem)}{req.json["endpoint"]}'
                other_node_name = mem
                sender(url, json=req.json['payload'], **nx.auth.get_requests_auth(other_node_name))

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

        # dict connection_request_id -> ConnectionHandshake
        connection_requests = {}

        # This request instructs node to start connecting to other node
        # Arguments (json): name, address
        # After connection happens it needs to be approved by user
        # This will be an entry in /connect/pending
        @nx.app.route('/connect/start', methods=['POST'])
        @nx.httpauth.login_required
        def start_connecting():
            my_name = conf.name
            my_certificate = str(open(f"certs/{conf.name}.crt").read())
            other_node_name = req.json['name']
            other_node_address = req.json['address']

            conn_request_id = Authorization.generate_random_password()
            connection_requests[conn_request_id] = ConnectionHandshake(my_name)
            cur_handshake = connection_requests[conn_request_id]
            cur_handshake.other_node_address = other_node_address
            cur_handshake.other_name = other_node_name

            requests.post(f"https://{other_node_address}/connect/request",
                        json={
                            'id': conn_request_id,
                            'name': my_name,
                            'cert': my_certificate,
                            'port': nx.conf['port']
                        }, verify=False)

            return ''

        # Connection request (in json)
        # cert: .crt file as string
        # name: name of node requesting connection
        # id: identification string of this request
        # port: other node port
        @nx.app.route('/connect/request', methods=['POST'])
        def connection_request():
            # TODO - check that conn_request_id is just letters a-z or we got an exploit xd
            conn_request_id = str(req.json['id'])
            other_node_name = str(req.json['name'])
            other_node_port = str(req.json['port'])
            other_node_certificate = str(req.json['cert'])
            my_name = conf.name

            connection_requests[conn_request_id] = ConnectionHandshake(my_name)
            cur_handshake = connection_requests[conn_request_id]
            cur_handshake.other_certificate = other_node_certificate
            cur_handshake.other_name = other_node_name
            cur_handshake.other_node_address = f"{req.remote_addr}:{other_node_port}"

            other_cert_file_path = f"certs/tmp_{conn_request_id}.crt"
            cert_file = open(other_cert_file_path, "w")
            cert_file.write(other_node_certificate)
            cert_file.close()

            requests.post(f"https://{cur_handshake.other_node_address}/connect/response",
                          json={
                              'cert': cur_handshake.my_certificate,
                              'token': cur_handshake.access_token_to_me,
                              'id': conn_request_id
                          }, verify=other_cert_file_path)

            return ''

        # Connection request response (json)
        # cert: other node's certificate
        # token: acces token for other node
        # id: identification string of this request
        @nx.app.route('/connect/response', methods=['POST'])
        def connection_request_response():
            # TODO - check that conn_request_id is just letters a-z or we got an exploit xd
            other_certificate = str(req.json['cert'])
            token_for_other = str(req.json['token'])
            conn_request_id = str(req.json['id'])

            cur_handshake = connection_requests[conn_request_id]

            cur_handshake.other_certificate = other_certificate
            cur_handshake.access_token_to_other = token_for_other

            other_cert_file_path = f"certs/tmp_{conn_request_id}.crt"
            cert_file = open(other_cert_file_path, "w")
            cert_file.write(other_certificate)
            cert_file.close()

            requests.post(f"https://{cur_handshake.other_node_address}/connect/finish",
                          json={
                              'id': conn_request_id,
                              'token': cur_handshake.access_token_to_me
                          }, verify = other_cert_file_path)

            return ''

        # Finish connection request
        # token: access token to other node
        # id: identification string of this request
        @nx.app.route('/connect/finish', methods=['POST'])
        def connection_finish():
            # TODO - check that conn_request_id is just letters a-z or we got an exploit xd
            conn_request_id = str(req.json['id'])
            access_token_to_other = str(req.json['token'])

            cur_handshake = connection_requests[conn_request_id]
            cur_handshake.access_token_to_other = access_token_to_other

            return ''

        # Gets list of pending connections
        # Each connection is a dict {'nodeName': str, 'hash': str}
        # User should confirm that hashes are the same on nodes willing to connect
        # And then do /connect/accept
        @nx.app.route('/connect/pending', methods=['GET'])
        @nx.httpauth.login_required
        def get_pending_connections():
            pending_connections = []

            for handshake in connection_requests.values():
                if(handshake.is_complete()):
                    pending_connections.append({
                        'nodeName': handshake.other_name,
                        'hash': handshake.get_hash()
                    })

            return {'conns': pending_connections}

        # This is used to accept a pending connection request
        # hash: hash of pending connection that should be accepted
        @nx.app.route('/connect/accept', methods=['POST'])
        @nx.httpauth.login_required
        def accept_connection():
            accepted_hash = req.json['hash']

            for handshake_id in connection_requests.keys():
                handshake = connection_requests[handshake_id]

                if(not handshake.is_complete() or handshake.get_hash() != accepted_hash):
                    continue

                new_node_name = handshake.other_name
                new_node_address = handshake.other_node_address

                nx.auth.add_user(new_node_name, handshake.access_token_to_me)
                nx.auth.add_access_token(new_node_name, handshake.access_token_to_other)

                new_node_cert_file = open(f"certs/{new_node_name}.crt", "w")
                new_node_cert_file.write(handshake.other_certificate)
                new_node_cert_file.close()

                del connection_requests[handshake_id]

                return ''

            return 404