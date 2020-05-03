import unittest
from multiprocessing import Process
from tests.node_instance import NodeInstance
import requests
import time
import json

class TestNodeDaemon(unittest.TestCase):
    def setUp(self):
        self.nodeA = NodeInstance()
        self.port = 5000

        time.sleep(2) # Wait for node to initialize
        # TODO redirect server output to log file


    def testName(self):
        response = requests.get(f"http://localhost:{self.port}/api/name")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "nodeA")

    def testDoCommand(self):
        response = requests.post(f"http://localhost:{self.port}/api/docommand", data={'cmd':'script_a'})

        self.assertEqual(response.status_code, 200)
        

    def testDoCommandMissingParameter(self):
        response = requests.post(f"http://localhost:{self.port}/api/docommand", data={})

        self.assertEqual(response.status_code, 400) # missing parameter


    def testSendCommand(self):
        response = requests.post(f"http://localhost:{self.port}/api/sendcommand", data={'cmd':"script_a", 'target':"nodeA"})
            
        self.assertEqual(response.status_code, 200)


    def testSendComandMissingParameter(self):
        response = requests.post(f"http://localhost:{self.port}/api/sendcommand")
            
        self.assertEqual(response.status_code, 400)

        
    def testSendComandBadTarget(self):
        response = requests.post(f"http://localhost:{self.port}/api/sendcommand", data={'cmd':"correct command", 'target':"not existing node"})

        self.assertEqual(response.status_code, 400)

    def tearDown(self):
        del self.nodeA
