from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_httpauth import HTTPBasicAuth
from dataclasses import dataclass
import argparse as ap
import yaml
from .net.network import Network
from .net.authorization import Authorization

class Nexus:
    app: Flask
    cors: CORS
    conf: any
    api: Api
    httpauth: HTTPBasicAuth
    auth: Authorization

    def __init__(self):
        parser = ap.ArgumentParser('node')
        parser.add_argument('config', default='config.yaml', nargs='?',
            help='path to the static config file')

        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.cors = CORS(self.app)
        self.httpauth = HTTPBasicAuth()
        args = parser.parse_args()
        try:
            data = open(args.config, 'r').read()
            self.conf = yaml.load(data, Loader=yaml.FullLoader)
        except:
            self.conf = {}

        self.auth = Authorization(self.conf['net']['name'])

