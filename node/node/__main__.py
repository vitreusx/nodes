from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os.path import dirname

app = Flask(__name__)
pwd = dirname(__file__)

app.config['SQLALCHEMY_BINDS'] = {
    'net': f'sqlite:///{pwd}/db/net.db'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from .modules.net import install
install(app)

app.run(port = 8080)