import unittest
from multiprocessing import Process
from tests.node_instance import NodeInstance
import requests
import time
import json
import shutil

def reset_config(config_name):
    shutil.copyfile(config_name + '_base.yaml', config_name + '.yaml')

class TestNodeDaemonConnection(unittest.TestCase):
    def setUp(self):
        #reset configs
        reset_config("tests/data/config_noded_a")
        reset_config("tests/data/config_noded_b")
        reset_config("tests/data/config_noded_c")

        self.nodeA = NodeInstance("tests/data/config_noded_a.yaml")
        self.portA = 5000
        self.nameA = 'nodeA'

        self.nodeB = NodeInstance("tests/data/config_noded_b.yaml")
        self.portB = 5001
        self.nameB = 'nodeB'

        self.nodeC = NodeInstance("tests/data/config_noded_c.yaml")
        self.portC = 5002
        self.nameC = 'nodeC'

        time.sleep(2) # Wait for node to initialize
        # TODO redirect server output to log file


    def testConnect(self):
        # connect node B to node A
        response = requests.post(f"http://localhost:{self.portA}/api/connect", data={'port': self.portB, 'name': self.nameB})

        def assert_node_in_list(node_port, node_name, known_nodes):
            ''' assert that node with given port and name is in given list '''
            def node_equal(port, name, other):
                return int(other['port']) == port and other['name'] == name

            self.assertTrue(any([node_equal(node_port, node_name, node) for node in known_nodes]))
            
        nodesA = requests.get(f"http://localhost:{self.portA}/api/nodes")
        known_nodesA = json.loads(nodesA.text)

        assert_node_in_list(self.portA, self.nameA, known_nodesA)
        assert_node_in_list(self.portB, self.nameB, known_nodesA)

        nodesB = requests.get(f"http://localhost:{self.portB}/api/nodes")
        known_nodesB = json.loads(nodesB.text)

        print(known_nodesB)

        assert_node_in_list(self.portA, self.nameA, known_nodesB)
        assert_node_in_list(self.portB, self.nameB, known_nodesB)

    def tearDown(self):
        del self.nodeA
        del self.nodeB
        del self.nodeC
