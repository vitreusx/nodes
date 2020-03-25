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

app = Flask(__name__, static_folder='data/html')

# Print server output to file
logging.basicConfig(filename='server_logs.log', level=logging.DEBUG)

# API Requests
@app.route('/api/name', methods = ['GET'])
def on_api_name():
    return config.nodeName;

@app.route('/api/docommand', methods = ['POST'])
def on_api_docommand():
    command = request.values.get('cmd')
    print("Doing command " + str(command))

    if command in config.allowed_scripts:
        os.system(f"python3 scripts/{command}")
        return "OK", 200
    else:
        return "Script not allowed", 422

@app.route('/api/sendcommand', methods = ['POST'])
def on_api_sendcommand():
    command = request.values.get('cmd')
    target = request.values.get('target') 
    targetNode = [n for n in config.known_nodes if n['name'] == target][0]
    doRequest = requests.post(f"http://{targetNode['ip']}:{targetNode['port']}/api/docommand", data={'cmd': command})
    return "I dont know how to do that"

@app.route('/api/nodes', methods = ['GET'])
def on_api_nodes():
    # Send known nodes somehow, Json? Split by some character?
    return jsonify(config.known_nodes), 200

@app.route('/api/connect', methods = ['POST'])
def on_api_connect():
    new_node = dict()
    new_node['ip'] = request.environ.get('REMOTE_ADDR')
    new_node['port'] = request.values.get('port')
    new_node['name'] = request.values.get('name')

    if None in new_node.values():
        return "Missing Parameter", 201

    for node in config.known_nodes: # This node sends it also to itself. Is it ok?
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

    if new_node not in config.known_nodes:
        config.known_nodes.append(new_node)
    
    return "ADDED", 200

@app.route('/') # Serves web interface
def home():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    con = sql.connect(config.db_path)
    app.run(port = config.port)
