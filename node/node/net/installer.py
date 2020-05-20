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

        @nx.app.route('/net/groups', methods=['GET'])
        def groups():
            return json.dumps(network.groups())

        class Group(Resource):
            def get(self, group):
                return network.group(group).members()
            
            def put(self, group):
                if not network.create(group):
                    return False
                network.group(group).invite(conf.name, conf.addr)
            
            def delete(self, group):
                return network.erase(group)

        nx.api.add_resource(Group, '/net/g/<group>', endpoint='api.group')
        
        class Member(Resource):
            def group(self, group):
                rv = network.group(group)
                if not rv:
                    abort(404, f'Group {group} does not exist.')
                return rv
            
            def get(self, group, member):
                g = self.group(group)
                return g.members(member)
            
            def put(self, group, member):
                g = self.group(group)
                return g.invite(member)
            
            def delete(self, group, member):
                g = self.group(group)
                return g.kick(member)

        nx.api.add_resource(Member, '/net/g/<group>/m/<member>', endpoint='api.member')

        @nx.app.route('/net/g/<group>/leave', methods=['POST'])
        def leave(group):
            g = network.db.get(group)
            if not g:
                abort(404, f'Group {group} does not exist.')
            ur = url_for('api.member', group=group, member=g['local'], _external=True)
            r = requests.delete(ur)
            return r.content, r.status_code