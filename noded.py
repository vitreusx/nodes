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
import config
import logging
import os
import speech_recognition as sr
from multiprocessing import Process
from nodemanager import NodeManager;

nodeManager = NodeManager()

app = Flask(__name__, static_folder='data/html')

# Print server output to file
logging.basicConfig(filename='server_logs.log', level=logging.DEBUG)

# API Requests
@app.route('/api/name', methods = ['GET'])
def on_api_name():
    return nodeManager.get_name()

@app.route('/api/docommand', methods = ['POST'])
def on_api_docommand():
    command = request.values.get('cmd')

    if command is None:
        return "Missing parameter", 400
    
    print("Doing command " + str(command))

    if nodeManager.do_command(command):
        return "OK", 200
    else:
        return "Script not allowed", 403

@app.route('/api/sendcommand', methods = ['POST'])
def on_api_sendcommand():
    command = request.values.get('cmd')
    target = request.values.get('target') 

    if command is None or target is None:
        return "Missing parameter", 400

    try:
        targetNode = [n for n in nodeManager.get_known_nodes() if n['name'] == target][0]
    except IndexError:
        return "Bad target", 400

    doRequest = requests.post(f"http://{targetNode['ip']}:{targetNode['port']}/api/docommand", data={'cmd': command})

    if doRequest.status_code != 200:
        return "Sending command falied", doRequest.status_code
    
    return "Message sent", 200

@app.route('/api/nodes', methods = ['GET'])
def on_api_nodes():
    return jsonify(nodeManager.get_known_nodes()), 200

@app.route('/api/connect', methods = ['POST'])
def on_api_connect():
    new_node = dict()
    new_node['ip'] = request.environ.get('REMOTE_ADDR')
    new_node['port'] = request.values.get('port')
    new_node['name'] = request.values.get('name')

    if None in new_node.values():
        return "Missing Parameter", 201

    for node in nodeManager.get_known_nodes(): # This node sends it also to itself. Is it ok?
        result = requests.post(f"http://{node['ip']}:{node['port']}/api/addnode", data=new_node)
        # TODO what if this fails?

    return "ADDED", 200

@app.route('/api/addnode', methods = ['POST'])
def on_api_addnode():
    # TODO authentication
    new_node = dict()
    new_node['ip'] = request.values.get('ip')
    new_node['port'] = request.values.get('port')
    new_node['name'] = request.values.get('name')
    
    # This check is not needed when authentication will be added
    if None in new_node.values():
        return "Missing Parameter", 201

    nodeManager.add_known_node(new_node['name'], new_node['ip'], new_node['port'])
    return "ADDED", 200

@app.route('/') # Serves web interface
def home():
    return app.send_static_file('index.html')

cloud_cred = open('google-cloud.json').read()

def cb(rec, audio):
    try:
        command = rec.recognize_google_cloud(audio, credentials_json=cloud_cred).strip()
        print(command)
        nodeManager.do_command(command)

    except:
        pass

def voice_thread_fn():
    rec = sr.Recognizer()
    mic = sr.Microphone()

    with mic as src:
        rec.adjust_for_ambient_noise(src, duration=1)

    while True:
        with mic as src:
            audio = rec.listen(src, phrase_time_limit=5)
            cb(rec, audio)

if __name__ == '__main__':
    voice_thr = Process(target=voice_thread_fn)
    voice_thr.start()
    app.run(port = nodeManager.get_port())
