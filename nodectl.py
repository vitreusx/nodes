"""
nodectl is a command line interface for nodedaemon
"""
import requests 

nodedAddress = "http://localhost:5000"

def command_help():
    print("do <command> - do command on connected noded")
    print("send <command> <name> - send command to other node with given name")

def command_do(command):
    doRequest = requests.post(f"{nodedAddress}/api/docommand", data={'cmd': command})

def command_send(command, name):
    sendRequest = requests.post(f"{nodedAddress}/api/sendcommand", data={'cmd': command, 'target': name})
    return

def connect_to(node):
    result = request.post(f"{node['ip']}:{node['port']}/api/connect}", data={'port':config.port, 'name':config.name})
    
if __name__ == '__main__':
    print("Connecting to noded...");
    nameRequest = requests.get(f"{nodedAddress}/api/name")
    
    if nameRequest.status_code != 200:
        print(f"ERROR: response status: {nameRequest.status_code}, text: {nameRequest.text}")

    nodeName = nameRequest.text
    print(f"Succesfully connected to noded with name '{nodeName}'")
    print("Starting command line - type 'help' for help")

    while True:
        print("> ", end="")
        command = input()
        print("Doing the command: " + command)

        if(command == "help"):
            command_help()
        
        cmd = command.split(' ')

        if(cmd[0] == "do"):
            command_do(cmd[1])

        if(cmd[0] == "send"):
            command_send(cmd[1], cmd[2])
