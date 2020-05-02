from flask import Blueprint
import yaml

class Router:
    def __init__(self, db, conf):
        self.router = Blueprint('net', __name__)

        @self.router.record
        def init_router(state):
            global app
            app = state.app

        @self.router.route('/name')
        def get_name():
            return conf['name']

        @self.router.route('/groups')
        def list_groups():
            pass

        @self.router.route('/reset')
        def reset_conf():
            pass

        @self.router.route('/group/<group>/create')
        def create_group():
            pass

        @self.router.route('/group/<group>/destroy')
        def destroy_group():
            pass

        @self.router.route('/group/<group>/join')
        def join_group():
            pass

        @self.router.route('/group/<group>/leave')
        def leave_group():
            pass

        @self.router.route('/group/<group>/list')
        def list_members():
            pass

        @self.router.route('/group/<group>/proxy')
        def proxy():
            pass
