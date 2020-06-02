import shelve

"""
    Authorization works using users
    There is a set of authorized users that are allowed to use this node
    Other nodes present their name and accessToken as username and password
    There is an user named 'local' with random password that local interfaces use to authorize

"""

class Authorization:
    def __init__(self):
        # db['users'] is a dict username -> password of trusted users
        # db['tokens'] is a dict nodeName -> accessToken keeping this node's access tokens to other nodes
        self.db = shelve.open('db/auth.db', writeback=True)

        if(not self.db.has_key('users')):
            self.db = {'users': {}, 'tokens': {}}

        if(not self.db['users'].has_key('local')):
            self.db['users']['local'] = "12345" # TODO - change to random

    def validate_user(self, username, password):
        if(not self.db['users'].has_key(username)):
            return False

        return (self.db[username] == password)

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