from ..nexus import Nexus
from .config import Config
from .network import Network
from flask import request as req, abort
import json

class Installer:
    def validate(self, required):
        if not req.json \
            or any(param not in req.json \
                    for param in required):
            abort(404)
    
    def group(self):
        rv = self.network.group(req.json['group'])
        if not rv:
            abort(204)
        return rv

    def __init__(self, nx: Nexus):
        self.nx = nx
        self.conf = Config(nx.conf.get('net') or {})
        self.network = Network(self.conf)

        @nx.app.route('/net/list', methods=['GET'])
        def list_groups():
            return json.dumps(self.network.groups())

        @nx.app.route('/net/group', methods=['PUT'])
        def create_group():
            self.validate(['group'])
            
            if self.network.create(req.json['group']):
                return '', 201
            else:
                return 'Group exists', 400

        @nx.app.route('/net/group', methods=['DELETE'])
        def delete_group():
            self.validate(['group'])
            
            if self.network.erase(req.json['group']):
                return ''
            else:
                return 'No such group exists', 204

        @nx.app.route('/net/group/members', methods=['GET'])
        def list_members():
            self.validate(['group'])
            group = self.group()
            
            return json.dumps(group.members())

        @nx.app.route('/net/group/member', methods=['PUT'])
        def invite_member():
            self.validate(['group', 'name', 'addr'])
            group = self.group()
            
            if group.invite(req.json['name'], req.json['addr']):
                return '', 201
            else:
                return 'Member already present', 400

        @nx.app.route('/net/group/member', methods=['DELETE'])
        def kick_member():
            self.validate(['group', 'name'])
            group = self.group()
            
            if group.kick(req.json['name']):
                return ''
            else:
                return 'No such member is present', 204
