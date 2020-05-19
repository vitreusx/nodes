from ..nexus import Nexus
import sys
import os
import importlib
from os.path import join, basename

class Installer:
    def __init__(self, nx: Nexus):
        for path in (nx.conf.get('local') or []):
            dir = join(os.getcwd(), path)
            sys.path.append(dir)

            mod = importlib.import_module(basename(dir))
            getattr(mod, 'Local')(nx)
