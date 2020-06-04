import readline
import requests
import json
import yaml
import os


class CommandLineInterface():
   
    def __init__(self):
        try:
            data = open('config.yaml', 'r').read()
            config = yaml.load(data, Loader=yaml.FullLoader)
            self.name = config['net']['name']
            self.port = config['net']['port']
        except:
            self.name = input('Please enter local node name: ')
            self.port = input('Please enter port of local node: ')

        self.password = input(f'Please enter password for {self.name}: ')
        self.target = self.name
        self.group = self.get_group(self.target)
        self.cert = str(os.path.join('certs', f'{self.name}.crt'))

        self.commands = {
            'do' : self.do_execute,
            'group' : self.do_group,
            'say-hello' : self.do_hello, 
            'help' : self.do_help, 
            'list' : self.do_list, 
            'voice' : self.do_voice,
            'conn':   self.do_conn,
            'quit': self.do_quit
        }
        
        def complter(text, state):
            options = [i for i in self.commands.keys() if i.startswith(text)]
            if state < len(options):
                return options[state]
            else:
                return None

        readline.parse_and_bind("tab: complete")
        readline.set_completer(complter)

        
    def prompt(self):
        return f'aurora {self.group}:{self.target}> '
        

    def evaluate_command(self, command):
        # TODO make case insensitive

        if len(command) == 0:
            return None

        handler = self.commands.get(command[0])
        if handler is None:
            raise ValueError('Unrecognized command')
 
        return handler(command[1:])


    def run_main_loop(self):
        while True:
            try:
                command = input(self.prompt()).split()
            except KeyboardInterrupt:
                print() # so that bash prompt is in newline
                quit()  
 
            try:
                response = self.evaluate_command(command)
                if response is not None:
                    print(response) 
            except ValueError as e:
                print(str(e))
 

    def get_group(self, node):
        auth = {
            'auth': ('local', self.password),
            'verify': str(os.path.join('certs', f'{self.name}.crt'))
        }
        
        groups = requests.get(f'https://127.0.0.1:{self.port}/net/groups', **auth).text
        groups = json.loads(groups)
        for group in groups:
            members = requests.get(f'https://127.0.0.1:{self.port}/net/g/{group}', **auth).text
            members = json.loads(members)
            if self.name in members:
                return group

        raise ValueError("Node doesn't have group") 


    # functions in self.commands have to have docstring as help


    def check_param_len(self, params, length):
        if len(params) < length:
            raise ValueError('Not enough parameters')
        if len(params) > length:
            raise ValueError('Too many parameters')
        
   
    def send_request(self, method, endpoint, data={}):
        try:
            json_dict = dict()
            json_dict['endpoint'] = endpoint 
            json_dict['method'] = method
            json_dict['payload'] = data
            json_dict['targets'] = {self.group: [self.target]}
            auth = {
                'auth': ('local', self.password),
                'verify': str(os.path.join('certs', f'{self.name}.crt'))
            }
            response = requests.post(f'https://127.0.0.1:{self.port}/net/proxy', json=json_dict, **auth) 
            response_text = json.loads(response.text)[0]
            if response.status_code != 200:
                return 'Operation Failed'
            else:
                return ('Success', response_text)
        except:
            return f'Failed to connect to target {self.target}'
            
    
    def do_execute(self, params):
        self.check_param_len(params, 1)
        return self.send_request('post', f'/voice/p/{params[0]}')
#        requests.post(f'http://{self.target}/voice/p/{params[0]}') 


    def do_group(self, params):
        '''Manage groups
           options:
           -a <group> <node> add node to group
           -r <group> <node> remove node from group
           -c <name> create new group
           -d <name> delete group 
           -m <name> list members of the group'''

        if len(params) == 0:
            raise ValueError('Option not  given')

        if params[0] == '-c':
            self.check_param_len(params[1:], 1)
            return self.send_request('put', f'/net/g/{params[1]}')[0]
            
        elif params[0] == '-d':
            self.check_param_len(params[1:], 1)
            return self.send_request('delete', f'/net/g/{params[1]}')[0]
        
        elif params[0] == '-a':
            self.check_param_len(params[1:], 2)
            return self.send_request('put', f'/net/g/{params[1]}/m/{params[2]}')[0]
            
        elif params[0] == '-r':
            self.check_param_len(params[1:], 2)
            return self.send_request('delete', f'/net/g/{params[1]}/m/{params[2]}')[0]
        elif params[0] == '-m':
            self.check_param_len(params[1:], 1)
            response = self.send_request('get', f'/net/g/{params[1]}')[1]
            members = [key + ' - ' + value for key, value in json.loads(response).items()]
            return '\n'.join(members)

        else:
            raise ValueError('Wrong option')


    def do_hello(self, params):
        ''' Say hello. No params required to say hello! '''
        return 'hello'
 

    def do_help(self, params):
        ''' Print available commands, and their description '''
        # TODO is it good idea to print __doc__ as help?
        for key, value in self.commands.items():
            print('{0: <10}'.format(key), '-', value.__doc__)


    def do_list(self, params):
        ''' -g List groups (default)
            -v List voice commands '''
        if len(params) > 1:
            raise ValueError('Too many parameters')

        if len(params) == 0 or params[0] == '-g':
            response = self.send_request('get', f'/net/groups')[1]
            groups = json.loads(response)
            return '\n'.join(groups)

        elif params[0] == '-v':
            response = self.send_request('get','/voice/phrases')
            groups = json.loads(response)
            return '\n'.join(groups)

        else:
            raise ValueError('Wrong option') 


    def do_voice(self, params):
        ''' Manage voice commands
            -a <command> <endpoint> <payload> Add new voice command
            -r <command> Remove voice command '''
        if len(params) == 0:
            raise ValueError('Option not given')

        if params[0] == '-a':
            self.check_param_len(params[1:], 3)
            data = {'endpoint': '/tasks/' + params[2], 'payload': params[3]}
            return self.send_request('put', f'/voice/p/{params[1]}', data)[0]

        elif params[0] == '-r':
            self.check_param_len(params[1:], 1)
            return self.send_request('delete', f'/voice/p/{params[1]}')

        else:
            raise ValueError('Wrong option') 
        
    def do_conn(self, params):
        ''' Manage secure connections from/to this node
            -c <nodeName> <nodeAdress> Initiate connection to this node
            -p See pending connections with their hashes
            -a <hash> Accept connection with given hash '''

        if len(params) == 0:
            raise ValueError('Option not given')

        if params[0] == '-c':
            self.check_param_len(params[1:], 2)
            nodeName = params[1]
            nodeAddr = params[2]

            resp = requests.post(f"https://127.0.0.1:{self.port}/connect/start", json={
                'name': nodeName,
                'address': nodeAddr
            }, 
            auth = ('local', self.password),
            verify=self.cert)

        if params[0] == '-p':
            resp = requests.get(f"https://127.0.0.1:{self.port}/connect/pending", auth = ('local', self.password), verify=self.cert)
            print(resp.text)

        if params[0] == '-a':
            self.check_param_len(params[1:], 1)
            accepted_hash = params[1]
            requests.post(f"https://127.0.0.1:{self.port}/connect/accept", 
                          json={
                              'hash': accepted_hash
                          },
                          auth = ('local', self.password), verify=self.cert)
            
    def do_quit(self, params):
        ''' Quit program '''
        quit()
