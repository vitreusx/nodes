from flask import Flask
from flask_cors import CORS
from dataclasses import dataclass
import argparse as ap
import yaml
from .net.network import Network

class Nexus:
    app: Flask
    cors: CORS
    conf: any

    def __init__(self):
        parser = ap.ArgumentParser('node')
        parser.add_argument('config', default='config.yaml', nargs='?',
            help='path to the static config file')

        self.app = Flask(__name__)
        self.cors = CORS(self.app)
        args = parser.parse_args()
        try:
            data = open(args.config, 'r').read()
            self.conf = yaml.load(data, Loader=yaml.FullLoader)
        except:
            self.conf = {}
