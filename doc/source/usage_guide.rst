.. _usage_guide:

***********
Usage Guide
***********

Installing required packages
============================

| To run Aurora you will need the packages listed in the `requirements.txt` file.
| To install the packages (preferably in a virtual environment) type: 
::
    
    pip3 install requirements.txt
    
Configuring a local node
======================
| Aurora is a network of nodes running on different machines.
| You must configure the node to give it the addresses of other nodes as well as information on what commands it can run.
| The options include:
* nodeName
    The name that will be used to refer to this node. You have to modify it because having multiple nodes with the same name in the network might cause problems.
* port
    The port on which the node will be visible to the others in the network. By default it's 5000. You don't need to modify it unless you plan to run multiple nodes on the same machine.
* known_nodes
    | A persistent list of known nodes. 
    | Entries are of form `{'name': 'nodeA', 'ip': "127.0.0.1", 'port': 5000}`.
    | Nodes added here are known on startup.
* allowed_scripts
    A list of commands available to execute on this node.

Running the node
================
To run the node run the command:
::
    
    python3 nodectl.py

| If everything goes well, you will be moved to a command line to control this node.
| Available commands:
* help
    | Shows the available commands along with their usages.
* do <command> 
    | Runs a script from config with matching name as this node.
* send <command> <nodeName>
    | Runs a script on the node with the given name.
 

