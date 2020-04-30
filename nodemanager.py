import config;

class NodeManager:
    # TODO - replace with a database
    nodeName = "nameNotSet"
    known_nodes = []
    node_port = 4321

    text_commands = []
    voice_commands = []

    recognize_voice = False

    __init__(self):
        self.nodeName = config.nodeName
        self.known_nodes = config.known_nodes
        self.allowed_scripts = config.allowed_scripts
        self.recognize_voice = config.recognize_voice

    # Name
    def get_name(self):
        return self.nodeName

    def set_name(self, newName):
        self.nodeName = newName

    # Port
    def get_port(self):
        return node_port

    def set_port(self, new_port):
        self.node_port = new_port

    # Known nodes
    def get_known_nodes(self):
        return self.known_nodes

    def add_known_node(self, node_name, node_ip, node_port):
        new_node = {'name': node_name, 'ip': node_ip, 'port': node_port}

        if not new_node in self.known_nodes:
            self.known_nodes.append(new_node)

    def remove_known_node(self, node_name):
        known_nodes = [node for node in known_nodes if node['name'] != node_name]

    # Commands
    def do_text_command(self, command):
        result = False
        for (voice_command, script) in self.text_commands:
            if(voice_command == command)
                os.system(f"python3 scripts/{script}")
                result = True

        return result
                

    def do_voice_command(self, command):
        result = False
        for (voice_command, script) in self.voice_commands:
            if(voice_command == command)
                os.system(f"python3 scripts/{script}")
                result = True

        return result

    def get_text_commands(self):
            return self.text_commands

    def get_voice_commands(self):
            return self.voice_commands

    # Voice
    def should_recoginze_voice(self):
        return self.recognize_voice

    def set_recognize_voice(self, should_recoginze):
        self.recognize_voice = should_recoginze