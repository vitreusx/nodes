import readline
import requests
import json


class CommandLineInterface():
   
    def __init__(self):
        # TODO something more reasonable
        self.target = 'localhost:8080'
        self.commands = {
            'do' : self.do_execute,
            'group' : self.do_group,
            'hello' : self.do_hello, 
            'help' : self.do_help, 
            'list' : self.do_list, 
            'voice' : self.do_voice,
            'quit' : self.do_quit, 
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
        return 'aurora > '
        

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
 

    # functions in self.commands have to have docstring as help


    def check_param_len(self, params, length):
        if len(params) < length:
            raise ValueError('Not enough parameters')
        if len(params) > length:
            raise ValueError('Too many parameters')
        
    
    def send_request(self, request_func, url, **kwargs):
        try:
            response = request_func(url, kwargs) 
            if response.status_code != 200:
                return 'Operation Failed'
            else:
                return 'Success'
        except:
            return f'Failed to connect to target {self.target}'
            
    
    def do_execute(self, params):
        self.check_param_len(params, 1)
        command = requests.get(f'http://{self.target}/voice/phrase', json={'phrase': params[0]})
        if command.status_code != 200:
            return 'No such command'
        phrase = json.loads(command.text)
        endpoint = phrase['endpoint']
        requests.post(f'http://{self.target}{endpoint}') 


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
            # add group named params[1]
            # TODO check name
            return self.send_request(requests.put, f'http://{self.target}/net/g/{params[1]}')
            
        elif params[0] == '-d':
            self.check_param_len(params[1:], 1)
            # add group named params[1]
            # TODO check name
            return self.send_request(requests.delete, f'http://{self.target}/net/g/{params[1]}')
        
        elif params[0] == '-a':
            self.check_param_len(params[1:], 2)
            return self.send_request(requests.put, f'http://{self.target}/net/g/{params[1]}/m/{params[2]}') 
            
        elif params[0] == '-r':
            self.check_param_len(params[1:], 2)
            return self.send_request(requests.delete, f'http://{self.target}/net/g/{params[1]}/m/{params[2]}') 
        elif params[0] == '-m':
            self.check_param_len(params[1:], 1)
            try:
                response = requests.get(f'http://{self.target}/net/g/{params[1]}') 
                if response.status_code != 200:
                    return 'Operation Failed'
                else:
                    members = [key + ' - ' + value for key, value in json.loads(response.text).items()]
                    return '\n'.join(members)
            except:
                return f'Failed to connect to target {self.target}'

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
            try:
                groups = json.loads(requests.get(f'http://{self.target}/net/groups').text)
                return '\n'.join(groups)
            except:
                return f'Failed to connect to target {self.target}'

        elif params[0] == '-v':
            try:
                groups = json.loads(requests.get(f'http://{self.target}/voice/phrases').text)
                return '\n'.join(groups)
            except:
                return f'Failed to connect to target {self.target}'

        else:
            raise ValueError('Wrong option') 


    def do_voice(self, params):
        ''' Manage voice commands
            -a <command> <endpoint> <payload> Add new voice command
            -r <command> Remove voice command '''
        if len(params) == 0:
            raise ValueError('Option not  given')

        if params[0] == '-a':
            self.check_param_len(params[1:], 3)
            data = {'phrase': params[1], 'endpoint': '/tasks/' + params[2], 'payload': params[3]}
            return requests.put(f'http://{self.target}/voice/phrase', json = data).text

        elif params[0] == '-r':
            self.check_param_len(params[1:], 1)
            data = {'phrase': params[1]}
            return requests.delete(f'http://{self.target}/voice/phrase', json = data).text
            return self.send_request(requests.delete, f'http://{self.target}/voice/phrase', json = data)

        else:
            raise ValueError('Wrong option') 
        

    def do_quit(self, params):
        ''' Quit program '''
        quit()
