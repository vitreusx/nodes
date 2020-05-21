import unittest
from node_cli.cli import CommandLineInterface
import requests
import time
import json

class TestCli(unittest.TestCase):

    def setUp(self):
        self.cli = CommandLineInterface()

    def cli_call(self, func, params, expect):
        res = func(params)
        self.assertEqual(res, expect)
    
    def test_group_add(self):
        self.cli_call(self.cli.do_group, ['-c', 'grupa1'], 'Success')
        self.cli_call(self.cli.do_group, ['-c', 'grupa2'], 'Success')
        self.cli_call(self.cli.do_group, ['-c', 'grupa3'], 'Success')

        self.cli_call(self.cli.do_list, [], 'grupa1\ngrupa3\ngrupa2')

    def test_group_remove(self):
        self.cli_call(self.cli.do_group, ['-d', 'grupa1'], 'Success')
        self.cli_call(self.cli.do_group, ['-d', 'grupa2'], 'Success')
        self.cli_call(self.cli.do_group, ['-d', 'grupa3'], 'Success')
        self.cli_call(self.cli.do_list, [], '')
