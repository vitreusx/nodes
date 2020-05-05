import argparse as ap
from .app import App
from os.path import exists
import yaml
from flask_cors import CORS

def parse_args():
    parser = ap.ArgumentParser()
    parser.add_argument('config', default = 'config.yaml', nargs = '?', 
        help = 'path to the config file')
    
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    try:
        config = yaml.load(open(args.config, 'r').read(), 
                           Loader=yaml.FullLoader)
    except:
        config = {}
    
    app = App(config)
    CORS(app.flask)
    app.flask.run(host = '0.0.0.0',
                  port = config.get('port') or 8080,
                  threaded = True)
