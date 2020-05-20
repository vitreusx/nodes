.. _usage_guide:

***********
Usage Guide
***********

Introduction
============
| Aurora is a set of interconneted nodes living on multiple machines
| To set it up you will need to copy this folder onto each machine, configure and run it

Installing required packages
============================
| To run Aurora you will need the packages listed in the `requirements.txt` file.
| To install the packages (preferably in a virtual environment) type: 
::
    
    pip3 install -r requirements.txt
    
Configuring a local node
======================
| You must configure the node to give it the addresses of other nodes as well as information on what commands it can run.
| Node config can be found in config.yaml
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
* TODO - add more here

Groups
======
| Nodes can be organized into groups
| When one 

Running the node
================
To run the node run the command:
::
    
    python3 -m node

| If everything goes well, you will be moved to a command line to control this node.
| Available commands:
* help
    | Shows the available commands along with their usages.
* do <command> 
    | Runs a script from config with matching name as this node.
* send <command> <nodeName>
    | Runs a script on the node with the given name.
* TODO - add more here

Running the web interface
=========================
| Node can also be controled from a web interface
| To run the web interface you will need npm installed (version 6.14.5 works)
* Enter the ``/web`` directory
* On first use run ``npm install``
* To start the web interface run ``npm start``
* Enter shown address in your browser to access the interface

Speech recognition
==================
| You can toggle speech recogintion on/off by setting the option ``recognize_voice`` in config to ``1`` or ``0`` respectively
| When speech recognition is turned on it will listen for commands specified in the config and execute them once heard