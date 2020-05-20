****************
For Contributors
****************

| Each Aurora node has an http server running in the background. This
server is responsible for communication with other nodes and executing
commands in its own node.

Project design overwiev
=======================
* Code for node is ``/node`` directory
   * Node is a typical Flask app
* Code for web interface is in ``\web`` directory
   * Web interface is made using React

Node http API:
==============
.. function:: GET /net/groups

   Requests list of groups for this node

   :return: 200 Ok - Gives List[str]
   :return: 401 Unauthorized

.. function:: PUT /net/groups

   Create a new group on this node

   :return: 201 Created
   :return: 400 Bad Request - when group already exists

.. function:: DELETE /net/group

   Remove group from this node

   :return: 200 Ok
   :return: 204 No Content - When group doesn't exist
   :return: 401 Unauthorized

.. function:: GET /net/group/members

   List group members on this node

   :param group: - requested group

   :return: 200 Ok - Dict[str, str] (member_name, member_addr)
   :return: 401 Unauthorized

.. function:: PUT /net/group/member

   Add node to the group

   :param group:
   :param name:
   :param addr:

   :return: 201 Created
   :return: 400 Bad Request - When this member already exists
   :return: 401 Unauthorized

.. function:: DELETE /net/group/member

   Remove node from a group

   :param group:
   :param name:

   :return: 200 Ok
   :return: 401 Unauthorized

.. function:: POST /net/group/leave

   :param group:

   :return: 200 Ok
   :return: 401 Unauthorized

| Add more stuff here as api stabilizes

Running tests
=============
| TODO

Creating tests
==============
| TODO

Creating documentation
======================
| Documentation is created using Sphinx
| All files are in the ``/doc`` directory
| After making changes online hosting must be updated

Security
========
| See issue for security plans
