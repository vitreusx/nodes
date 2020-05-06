from flask import Flask
from flask_cors import CORS
from os import makedirs
from os.path import join, realpath, dirname
import importlib

class App:
    def __init__(self, config):
        self.flask = Flask(__name__)
        CORS(self.flask)

        self.root = realpath(config.get('root') or '.')
        self.port = config.get('port') or 8080

        for mod_name, conf in (config.get('modules') or {}).items():
            mod = importlib.import_module(f'.modules.{mod_name}', package='node')
            mod.install(self, conf or {})

    def run(self):
        self.flask.run(host = '0.0.0.0',
                       port = self.port,
                       threaded = True)