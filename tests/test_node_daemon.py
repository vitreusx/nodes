import unittest
from multiprocessing import Process
from noded import app, nodeManager
import requests
import time
import json

class TestNodeDaemon(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = nodeManager.get_port()
        cls.server = Process(target=app.run, kwargs={'port':nodeManager.get_port()}) 
        cls.server.start() # TODO redirect server output to log file

        
    def testName(self):
        response = requests.get(f"http://localhost:{self.port}/api/name")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, nodeManager.get_name())

        
    def testDoCommand(self):
        response = requests.post(f"http://localhost:{self.port}/api/docommand", data={'cmd':'script_a.py'})

        self.assertEqual(response.status_code, 200)
        

    def testDoCommandMissingParameter(self):
        response = requests.post(f"http://localhost:{self.port}/api/docommand", data={})

        self.assertEqual(response.status_code, 400) # missing parameter


    def testSendCommand(self):
        response = requests.post(f"http://localhost:{self.port}/api/sendcommand", data={'cmd':"script_a.py", 'target':"nodeA"})
            
        self.assertEqual(response.status_code, 200)


    def testSendComandMissingParameter(self):
        response = requests.post(f"http://localhost:{self.port}/api/sendcommand")
            
        self.assertEqual(response.status_code, 400)

        
    def testSendComandBadTarget(self):
        response = requests.post(f"http://localhost:{self.port}/api/sendcommand", data={'cmd':"correct command", 'target':"not existing node"})

        self.assertEqual(response.status_code, 400)


    def testConnect(self):
        response = requests.post(f"http://localhost:{self.port}/api/connect", data={'port': 1234, 'name': 'new_node'})

        nodes = requests.get("http://localhost:5000/api/nodes")

        known_nodes = json.loads(nodes.text)

        def node_equal(other):
            return int(other['port']) == 1234 and other['name'] == 'new_node'

        # Assert that new node is in known_nodes
        self.assertTrue(any([node_equal(node) for node in known_nodes]))


    @classmethod
    def tearDownClass(cls):
        cls.server.terminate()
