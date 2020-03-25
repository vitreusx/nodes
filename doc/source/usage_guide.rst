.. _usage_guide:

***********
Usage Guide
***********

Installing required packages
============================

| To run Aurora you will need packages listed in the `requirements.txt` file.
| To install packages (preferably in a virtual environment) do: 
::
    
    pip3 install requirements.txt
    
Configuring local node
======================
| Aurora is a network of nodes running on different machines
| You must configure the node to tell it addresses of other nodes as well as what commands it can run
| Options include:
* nodeName
    Name that will be used to refer to this node. You have to modify it because having multiple nodes with the same name in the network might introduce problems
* port
    Port on which the node will be visible to others on the network. By default it's 5000. You don't need to modify it unless you plan to run multiple nodes on the same machine.
* known_nodes
    | Persistent list of known nodes. 
    | Entries are of form `{'name': 'nodeA', 'ip': "127.0.0.1", 'port': 5000}` 
    | Nodes added here are known on startup
* allowed_scripts
    List of commands available to execute on this node

Running the node
================
To run the node run the command:
::
    
    python3 nodectl.py

| If everything goes well you will be put into a command line to control this node
| Available commands:
* help
    | Shows commands along with their usages
* do <command> 
    | runs script from config with matching name as this node
* send <command> <nodeName>
    | runs script on node with given name
 

