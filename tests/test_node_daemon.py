import unittest
from multiprocessing import Process
from noded import app
import config
import requests
import time

class TestNodeDaemon(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = Process(target=app.run, kwargs={'port':config.port}) 
        cls.server.start() # TODO redirect server output to log file

        
    def testName(self):
        try:
            response = requests.get(f"http://localhost:{config.port}/api/name")
        except:
            self.assertTrue(False, "Failed to connect to daemon")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, config.nodeName)

        
    def testDoCommand(self):
        try:
            response = requests.post(f"http://localhost:{config.port}/api/docommand", data={'cmd':'correct command'}) # TODO change it to actual correct command when checking will be added
        except:
            self.assertTrue(False, "Failed to connect to daemon")

        self.assertEqual(response.status_code, 200)
        

    def testDoCommandMissingParameter(self):
        try:
            response = requests.post(f"http://localhost:{config.port}/api/docommand", data={})
        except:
            self.assertTrue(False, "Failed to connent to daemon")

        self.assertEqual(response.status_code, 201) # missing parameter


    def testSendComand(self):
        try:
            response = requests.post(f"http://localhost:{config.port}/api/sendcommand", data={'cmd':"correct command", 'target':"nodeA"})
        except:
            self.assertTrue(False, "Failed to connent to daemon")
            
        self.assertEqual(response.status_code, 200)


    def testSendComandMissingParameter(self):
        try:
            response = requests.post(f"http://localhost:{config.port}/api/sendcommand")
        except:
            self.assertTrue(False, "Failed to connent to daemon")
            
        self.assertEqual(response.status_code, 201)

        
    def testSendComandBadTarget(self):
        try:
            response = requests.post(f"http://localhost:{config.port}/api/sendcommand", data={'cmd':"correct command", 'target':"not existing node"})
        except:
            self.assertTrue(False, "Failed to connent to daemon")
            
        self.assertNotEqual(response.status_code, 200) # TODO What code should be returned?
        self.assertNotEqual(response.status_code, 500) 

        
    @classmethod
    def tearDownClass(cls):
        cls.server.terminate()
