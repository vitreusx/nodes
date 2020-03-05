"""
Node daemon works in the background
Command line and web interfaces connect to it with an API
Daemon handles node stuff and serves web interface
"""

from flask import Flask, request;
import sqlite3 as sql;

app = Flask(__name__, static_folder='data/html')

db_path = "data/noded_db.db"

@app.route('/') # Serves web interface
def home():
   return app.send_static_file('index.html')

@app.route('/command') # Receives command to execute
def on_command():
   command = request.args.get('cmd')
   return "Ok doing " + str(command) + "\n"

@app.route('/conn_request') # Request for connection
def on_connect_request():
   return "NO"

if __name__ == '__main__':
    con = sql.connect(db_path)
    app.run()
