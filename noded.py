"""
Node daemon works in the background
Command line and web interfaces connect to it with an API
Daemon handles node stuff and serves web interface
"""

from flask import Flask, request;
import sqlite3 as sql;
import click
from flask.cli import AppGroup
import requests
import config


app = Flask(__name__, static_folder='data/html')
# API Requests

@app.route('/api/name', methods = ['GET'])
def on_api_name():
    return config.nodeName;

@app.route('/api/docommand', methods = ['POST'])
def on_api_docommand():
    command = request.values.get('cmd')
    print("Doing command " + str(command))
    # Do the command
    return "OK"

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
    return "YES"

@app.route('/') # Serves web interface
def home():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    con = sql.connect(config.db_path)
    app.run(port = config.port)
