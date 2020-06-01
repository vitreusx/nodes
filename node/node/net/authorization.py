import shelve

class Authorization:
    def __init__(self):
        self.db = shelve.open('db/auth.db', writeback=True)

    def validate_user(self, username, password):
        if not (username and password):
            return False

        if(not self.db.has_key('master')):  # TODO - remove this
            self.db['master'] = 'masterpass'

        if(not self.db.has_key(username)):
            return False

        return self.db[username] == password

    def add_user(self, username, password):
        self.db[username] = password
    
    def remove_user(self, username):
        if(self.db.has(username)):
            del self.db[username]

    def get_user_list(self):
        return db.keys()

    def clear_users(self):
        self.db.clear()

