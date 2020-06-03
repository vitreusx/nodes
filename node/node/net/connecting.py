from .authorization import Authorization
import hashlib

class ConnectionHandshake:
    def __init__(self, node_name):
        self.my_name = node_name
        self.other_name = None
        self.my_certificate = str(open(f'certs/{node_name}.crt').read())
        self.other_certificate = None
        self.access_token_to_me = Authorization.generate_random_password()
        self.access_token_to_other = None
        self.other_node_address = None

    def is_complete(self) -> bool:
        if(self.other_name is None):
            return False

        if(self.other_certificate is None):
            return False

        if(self.access_token_to_other is None):
            return False

        if(self.other_node_address is None):
            return False

        return True

    def get_hash(self) -> str:
        return hashlib.sha256(str(sorted(self.as_strings())).encode('utf-8')).hexdigest()
    
    def as_strings(self) -> [str]:
        return [self.other_name, self.my_name, self.my_certificate, self.other_certificate, self.access_token_to_me, self.access_token_to_other]

    def get_debug(self):
        return f"""
                other_name: {self.other_name}
                my_certificate: {self.my_certificate}
                other_certificate: {self.other_certificate}
                access_token_to_me: {self.access_token_to_me}
                access_token_to_other: {self.access_token_to_other}
                other_node_address: {self.other_node_address}
                """