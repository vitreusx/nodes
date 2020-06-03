from node.nexus import Nexus
from flask import request as req
import webbrowser as wb

class Local:
    def __init__(self, nx: Nexus):
        @nx.app.route('/tasks/lights', methods=['POST'])
        @nx.auth.login_required
        def lights():
            print(f'New lights\' state: {req.json.get("state") or "N/A"}')
            return ''
