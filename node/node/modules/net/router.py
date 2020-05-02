from flask import Blueprint, request as req
from .models import Group, Node, Member
from .models.group import GroupSchema
import json
import requests

class Router:
    def __init__(self, db, conf):
        self.router = Blueprint('net', __name__)

        @self.router.route('/name')
        def get_name():
            return conf.get('name') or ''

        @self.router.route('/groups')
        def list_groups():
            names = [group.name for group in Group.query.all()]
            return json.dumps(names)

        @self.router.route('/group/<group>/update', methods = ['POST'])
        def update(group):
            payload = req.json or {}
            grp = Group.query.filter_by(name = group).first_or_404()
            grp.update(payload)
            
            db.session.commit()
            return ''

        @self.router.route('/group/<group>/create', methods = ['POST'])
        def create(group):
            grp = Group(name = group)
            db.session.add(grp)

            node = Node(addr = req.host)
            grp.members.append(node)

            db.session.commit()
            return ''

        @self.router.route('/group/<group>/destroy', methods = ['POST'])
        def destroy(group):
            grp = Group.query.filter_by(name = group).first_or_404()
            db.session.delete(grp)
            db.session.commit()
            return ''

        @self.router.route('/group/<group>/join', methods = ['POST'])
        def join(group):
            payload = req.json or {}
            grp = Group.query.filter_by(name = group).first_or_404()
            node = Node(addr = req.remote_addr)
            if 'alias' in payload:
                node.alias = payload.get('alias')
            grp.members.append(node)
            db.session.commit()
            return ''

        @self.router.route('/group/<group>/leave', methods = ['POST'])
        def leave(group):
            node = Node(addr = req.remote_addr)
            grp = Group.query.filter_by(name = group).first_or_404()
            grp.members.delete(node)
            db.session.commit()
            return ''

        @self.router.route('/group/<group>/members')
        def list_members(group):
            grp = Group.query.filter_by(name = group).first_or_404()
            return grp.members

        @self.router.route('/group/<group>/proxy', methods = ['GET', 'POST'])
        def proxy(group):
            payload = req.json or {}
            target = payload.get('target')
            target_node = Member.query.filter(
                Member.group == group and 
                (Member.node.addr == target or
                 Member.node.alias == target)).first_or_404()

            proc = requests.get if req.method == 'GET' else requests.post
            r = proc(f'http://{target_node.addr}{payload.get("command")}',
                     payload.get('payload'))
            return r.content, r.status_code, r.headers.items()
