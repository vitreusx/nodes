import unittest
from multiprocessing import Process
from tests.node_instance import NodeInstance
import requests
import time
import json

class TestNodeDaemonConnection(unittest.TestCase):
    def setUp(self):
        self.nodeA = NodeInstance("tests/data/config_noded_a.yaml")
        self.portA = 5000

        self.nodeB = NodeInstance("tests/data/config_noded_a.yaml")
        self.portB = 5001

        self.nodeC = NodeInstance("tests/data/config_noded_a.yaml")
        self.portC = 5002

        time.sleep(2) # Wait for node to initialize
        # TODO redirect server output to log file


    def testConnect(self):
        response = requests.post(f"http://localhost:{self.port}/api/connect", data={'port': 1234, 'name': 'new_node'})

        nodes = requests.get("http://localhost:5000/api/nodes")

        known_nodes = json.loads(nodes.text)

        def node_equal(other):
            return int(other['port']) == 1234 and other['name'] == 'new_node'

        # Assert that new node is in known_nodes
        self.assertTrue(any([node_equal(node) for node in known_nodes]))

    def tearDown(self):
        del self.nodeA
