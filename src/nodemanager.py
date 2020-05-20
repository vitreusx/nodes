import yaml
import os

class NodeManager:
    config_path = "config.yaml"
    db_file = "data/data.db"

    # Node data
    nodeName = "nameNotSet"
    node_port = 5000
    recognize_voice = False

    commands = []

    known_nodes = []

    def __init__(self, config_file_path = 'config.yaml'):
        self.config_path = config_file_path
        self.read_config()

    def read_config(self):
        the_file = open(self.config_path, 'r')
        config_yaml = yaml.safe_load(the_file)

        self.nodeName = config_yaml['settings']['name']
        self.node_port = config_yaml['settings']['port']
        self.recognize_voice = config_yaml['settings']['recognize_voice']

        self.commands = []
        for command in config_yaml['commands']:
            self.commands.append((command['command'], command['script']))

        self.known_nodes = []
        for known_node in config_yaml['known_nodes']:
            self.known_nodes.append(known_node)


    def write_config(self):
        config = {
            'settings': {
                'name': self.nodeName,
                'port': self.node_port,
                'recognize_voice': self.recognize_voice
            },
            'commands': [],
            'known_nodes': self.known_nodes
        }

        for (command, script) in self.commands:
            config['commands'].append({
                                    'command': command,
                                    'script': script
                                    })

        the_file = open(self.config_path, 'w')
        yaml.dump(config, the_file, 
                  default_flow_style=False, sort_keys=False)

    # Name
    def get_name(self):
        return self.nodeName

    def set_name(self, newName):
        self.nodeName = newName
        self.write_config()

    # Port
    def get_port(self):
        return self.node_port

    def set_port(self, new_port):
        self.node_port = new_port
        self.write_config()

    # Voice
    def should_recognize_voice(self):
        return self.recognize_voice

    def set_recognize_voice(self, should_recoginze):
        self.recognize_voice = should_recoginze
        self.write_config()

    # Commands
    def do_command(self, command):
        result = False
        for (voice_command, script) in self.commands:
            if(voice_command == command):
                os.system(f"python3 scripts/{script}")
                result = True

        return result

    def get_commands(self):
            return self.commands

    def add_command(self, command_name, command_script):
        self.commands.append((command_name, command_script))
        self.write_config()

    def remove_command(self, command_name):
        self.commands = [(name, script) for (name, script) in self.commands if name != command_name]
        self.write_config()

    # Known nodes
    def get_known_nodes(self):
        return self.known_nodes

    # Returns false if such node already exists and adding is not possible, true otherwise.
    def add_known_node(self, node_name, node_ip, node_port):
        new_node = {'name': node_name, 'ip': node_ip, 'port': node_port}

        if not new_node in self.known_nodes:
            self.known_nodes.append(new_node)
            self.write_config()
            return True
        else:
            return False

    # Returns false if no such node exists and removing is not possible, true otherwise.
    def remove_known_node(self, node_name):
        new_known_nodes = [node for node in self.known_nodes if node['name'] != node_name]
        if self.known_nodes == new_known_nodes: 
            return False
        else:
            self.known_nodes = new_known_nodes
            self.write_config()
            return True
