Node API
========

<<<<<<< HEAD
Each Aurora node has an http server running in the background. This
=======
Each Aurora node has a http server running in the background. This
>>>>>>> f9ecdf2b6ede3c986315ebed6208ed1e85d1770c
server is responsible for communication with other nodes and executing
commands in its own node. The server provides the following functionalities.


.. function:: home() /

   Settings page(not implemented yet)

.. function:: on_api_name() /api/name
   
   Request requires no parameters

   Returns name of node in plaintext

.. function:: on_api_docommand /api/docommand

   Runs given command in requested node

   :param cmd: command to run

   :return: 200 - Command ran succesfully
   :return: 400 - Missing parameter
   :return: 403 - Command not allowed (see allowed commands)

.. function:: on_api_sendcommand() /api/sendcommand
   
   Sends request for another node to /api/docommand

   :param cmd: command to be sent
   :param target: name of target node

   :return: *200* - When command was sent succesfully, and other node
                  replied with code *200* to *docommand* request
   :return: *400* - Some paramerers are missing or *target* is not
                  in *known_nodes* of sender (see known_nodes)
   :return: *other code* - If command was sent succesfully, but 
                  *docommand* request failed. This fail status code 
                  is returned

.. function:: on_api_nodes() /api/nodes
   
   Returns list of known nodes in json (see known nodes)

   No parameters are required

   :return: *200* - Returns list of known nodes as json string

.. function:: on_api_connect() /api/connect

   Connects current node to network requested node is in.
   Adds new node to every other node's *known_nodes* list
   using */api/addnode*.

   :param port: Port number *sender* node is listening on
   :param name: name of sender node

   :return: *200* - Node connected succesfully
   :return: *400* - Missing parameter

.. function:: on_api_addnode() /api/addnode

   Adds new node to known_nodes list. This method should be available
   only for trusted nodes. (Authentication not implemented yet)

   :param ip: IPv4 address of new node
   :param port: port number of new node
   :param name: name of new node

   :return: *200* - When succesfully added new node
   :return: *400* - Missing parameter
