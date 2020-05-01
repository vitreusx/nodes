import unittest
from nodemanager import NodeManager
import shutil

def reset_config():
        shutil.copyfile('tests/data/config_test_base.yaml', 'tests/data/config_test.yaml')

def new_man():
    return NodeManager('tests/data/config_test.yaml')

class TestNodeManager(unittest.TestCase):
    
    def testRead(self):
        # Tests config reading
        reset_config()
        nodeManager = new_man()

        # Read settings
        self.assertEqual(nodeManager.get_name(), "testName")
        self.assertEqual(nodeManager.get_port(), 7878)
        self.assertEqual(nodeManager.should_recognize_voice(), 1)

        # Read commands
        self.assertEqual(nodeManager.get_commands(),
            [
             ('command1', 'command1script.py'),
             ('command2', 'command2script.py')
            ])

        # Read known nodes
        self.assertEqual(nodeManager.get_known_nodes(),
            [
                {'name': 'testName2', 'ip': '1.2.3.4', 'port': 1429},
                {'name': 'otherTestName', 'ip': "5.5.1.3", 'port': 9342}
            ])

    def testModify(self):
        reset_config()
        nodeManager = new_man()

        # Change name
        self.assertEqual(nodeManager.get_name(), "testName")
        nodeManager.set_name("changedName")
        self.assertEqual(nodeManager.get_name(), "changedName")
        self.assertEqual(new_man().get_name(), "changedName")

        # Change port
        self.assertEqual(nodeManager.get_port(), 7878)
        nodeManager.set_port(9898)
        self.assertEqual(nodeManager.get_port(), 9898)
        self.assertEqual(new_man().get_port(), 9898)

        # Change voice config
        self.assertEqual(nodeManager.should_recognize_voice(), 1)
        nodeManager.set_recognize_voice(False)
        self.assertEqual(nodeManager.should_recognize_voice(), 0)
        self.assertEqual(new_man().should_recognize_voice(), False)

        # Add a command
        self.assertEqual(nodeManager.get_commands(),
            [
             ('command1', 'command1script.py'),
             ('command2', 'command2script.py')
            ])
        nodeManager.add_command('command3', 'script3.py')
        self.assertEqual(nodeManager.get_commands(),
            [
             ('command1', 'command1script.py'),
             ('command2', 'command2script.py'),
             ('command3', 'script3.py')
            ])
        self.assertEqual(new_man().get_commands(),
            [
             ('command1', 'command1script.py'),
             ('command2', 'command2script.py'),
             ('command3', 'script3.py')
            ])

        # Remove a command
        nodeManager.remove_command('command2')
        self.assertEqual(nodeManager.get_commands(),
            [
             ('command1', 'command1script.py'),
             ('command3', 'script3.py')
            ])
        self.assertEqual(new_man().get_commands(),
            [
             ('command1', 'command1script.py'),
             ('command3', 'script3.py')
            ])

        # Add known node
        self.assertEqual(nodeManager.get_known_nodes(),
            [
                {'name': 'testName2', 'ip': '1.2.3.4', 'port': 1429},
                {'name': 'otherTestName', 'ip': "5.5.1.3", 'port': 9342}
            ])
        nodeManager.add_known_node('addedNode', '5.6.7.8', 274)
        self.assertEqual(nodeManager.get_known_nodes(),
            [
                {'name': 'testName2', 'ip': '1.2.3.4', 'port': 1429},
                {'name': 'otherTestName', 'ip': "5.5.1.3", 'port': 9342},
                {'name': 'addedNode', 'ip': "5.6.7.8", 'port': 274}
            ])
        self.assertEqual(new_man().get_known_nodes(),
            [
                {'name': 'testName2', 'ip': '1.2.3.4', 'port': 1429},
                {'name': 'otherTestName', 'ip': "5.5.1.3", 'port': 9342},
                {'name': 'addedNode', 'ip': "5.6.7.8", 'port': 274}
            ])

        # Remove known node
        nodeManager.remove_known_node('testName2')
        self.assertEqual(nodeManager.get_known_nodes(),
            [
                {'name': 'otherTestName', 'ip': "5.5.1.3", 'port': 9342},
                {'name': 'addedNode', 'ip': "5.6.7.8", 'port': 274}
            ])

        