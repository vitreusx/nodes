import shelve
import os.path
import string
import secrets

"""
    Authorization works using users
    There is a set of authorized users that are allowed to use this node
    Other nodes present their name and accessToken as username and password
    There is an user named 'local' with random password that local interfaces use to authorize

"""

class Authorization:
    def __init__(self, node_name):
        # db['users'] is a dict username -> password of trusted users
        # db['tokens'] is a dict nodeName -> accessToken keeping this node's access tokens to other nodes
        self.db = shelve.open('db/auth.db', writeback=True)

        if(not 'users' in self.db):
            self.db = {'users': {}, 'tokens': {}}

        def generate_random_password():
            return ''.join(secrets.choice(string.ascii_letters) for i in range(16))

        if(not 'local' in self.db['users']):
            self.db['users']['local'] = generate_random_password()

        if(not node_name in self.db['users']):
            self.db['users'][node_name] = generate_random_password()

    def validate_user(self, username, password):
        if(not username in self.db['users']):
            return False

        return (self.db['users'][username] == password)

    def add_user(self, username, password):
        self.db['users'][username] = password
    
    def remove_user(self, username):
        if(self.db['users'].has(username)):
            del self.db[username]

    def get_local_user_pass(self):
        return self.db['users']['local']

    def get_user_list(self):
        return self.db['users'].keys()

    def clear_users(self):
        self.db['users'].clear()

    def add_access_token(self, nodeName, accessToken):
        self.db['tokens'][nodeName] = accessToken

    def get_access_token_for(self, nodeName):
        return self.db['tokens'].get(nodeName)

    def clear_access_tokens(self):
        self.db['tokens'].clear()

    # Checks if there is authorization data for a given node
    def has_requests_auth(self, node_name):
        # Ensure we have a password for this node
        if(not self.db['tokens'].has_value(node_name)):
            return False

        # Ensure we have a cert file for this node
        cert_path = os.path.join('certs', f"{node_name}.pem")

        if(not os.path.isfile(cert_path)):
            return False

        return True

    # Returns dict containing arguments that need to be passed to requests
    # use like: requests.get('...', **nx.auth.get_requests_auth('nodeA')))
    def get_requests_auth(self, node_name):
        print(f'getting request auth for: {node_name}')

        cert_path = os.path.join('certs', f"{node_name}.pem")

        return {'auth': (node_name, self.db['tokens'].get(node_name)),
                'verify': str(cert_path)}