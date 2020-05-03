"""
Node daemon works in the background
Command line and web interfaces connect to it with an API
Daemon handles node stuff and serves web interface
"""

from flask import Flask, request;
from flask import jsonify
import sqlite3 as sql;
import click
from flask.cli import AppGroup
import requests
import logging
import os
import speech_recognition as sr
from threading import Thread
from src.nodemanager import NodeManager;

class Node:
    def __init__(self, config_file = 'config.yaml', 
                       log_file = 'server_logs.log'):

        self.manager = NodeManager(config_file)
        logging.basicConfig(filename=log_file, level=logging.DEBUG) # Print server output to file

        self.app = Flask(__name__, static_folder='data/html')
        self.setup_app()

        if(self.manager.should_recognize_voice()):
            self.start_voice_recognition()

    def setup_app(self):
        # API Requests
        @self.app.route('/api/name', methods = ['GET'])
        def on_api_name():
            return self.manager.get_name()

        @self.app.route('/api/docommand', methods = ['POST'])
        def on_api_docommand():
            command = request.values.get('cmd')

            if command is None:
                return "Missing parameter", 400
            
            print("Doing command " + str(command))

            if self.manager.do_command(command):
                return "OK", 200
            else:
                return "Script not allowed", 403

        @self.app.route('/api/sendcommand', methods = ['POST'])
        def on_api_sendcommand():
            command = request.values.get('cmd')
            target = request.values.get('target') 

            if command is None or target is None:
                return "Missing parameter", 400

            try:
                targetNode = [n for n in self.manager.get_known_nodes() if n['name'] == target][0]
            except IndexError:
                return "Bad target", 400

            doRequest = requests.post(f"http://{targetNode['ip']}:{targetNode['port']}/api/docommand", data={'cmd': command})

            if doRequest.status_code != 200:
                return "Sending command falied", doRequest.status_code
            
            return "Message sent", 200

        @self.app.route('/api/nodes', methods = ['GET'])
        def on_api_nodes():
            return jsonify(self.manager.get_known_nodes()), 200

        @self.app.route('/api/connect', methods = ['POST'])
        def on_api_connect():
            new_node = dict()
            new_node['ip'] = request.environ.get('REMOTE_ADDR')
            new_node['port'] = request.values.get('port')
            new_node['name'] = request.values.get('name')

            if None in new_node.values():
                return "Missing Parameter", 201

            known_nodes = [node for node in self.manager.get_known_nodes()]

            for node in known_nodes:
                result = requests.post(f"http://{new_node['ip']}:{new_node['port']}/api/addnode", data=node)

            for node in known_nodes:
                result = requests.post(f"http://{node['ip']}:{node['port']}/api/addnode", data=new_node)

            return "ADDED", 200

        @self.app.route('/api/addnode', methods = ['POST'])
        def on_api_addnode():
            # TODO authentication
            new_node = dict()
            new_node['ip'] = request.values.get('ip')
            new_node['port'] = request.values.get('port')
            new_node['name'] = request.values.get('name')
            
            # This check is not needed when authentication will be added
            if None in new_node.values():
                return "Missing Parameter", 201

            self.manager.add_known_node(new_node['name'], new_node['ip'], new_node['port'])
            return "ADDED", 200

        @self.app.route('/') # Serves web interface
        def home():
            return app.send_static_file('index.html')

    def start_voice_recognition(self):

        def voice_thread_fn():
            cloud_cred = open('google-cloud.json').read()
            rec = sr.Recognizer()
            mic = sr.Microphone()

            with mic as src:
                rec.adjust_for_ambient_noise(src, duration=1)

            def cb(rec, audio):
                try:
                    command = rec.recognize_google_cloud(audio, credentials_json=cloud_cred).strip()
                    print(command)
                    self.self.manager.do_command(command)

                except:
                    pass

            while True:
                with mic as src:
                    audio = rec.listen(src, phrase_time_limit=5)
                    cb(rec, audio)

        self.voice_thr = Thread(target=voice_thread_fn)
        self.voice_thr.start()

    def run(self):
        self.app.run(port = self.manager.get_port())
    
if __name__ == '__main__':
    node = Node()
    node.run()
