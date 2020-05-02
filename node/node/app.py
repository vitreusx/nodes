from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import makedirs
from os.path import join, realpath, dirname
import importlib

class App:
    def ensure_fs(self, path):
        makedirs(dirname(path), exist_ok=True)

    def __init__(self, config):
        self.flask = Flask(__name__)
        self.flask.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.flask.config['SQLALCHEMY_BINDS'] = {}

        self.root = realpath(config.get('root') or '.')

        for mod_name, conf in (config.get('modules') or {}).items():
            mod = importlib.import_module(f'.modules.{mod_name}', package='node')
            mod.install(self, conf or {})
