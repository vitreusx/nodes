from .nexus import Nexus
from .net.installer import Installer as NetInst
from .voice.installer import Installer as VoiceInst

if __name__ == '__main__':
    nx = Nexus()
    NetInst(nx)
    VoiceInst(nx)
    nx.app.run(host='0.0.0.0', port=nx.conf.get('port') or 8080, threaded=True)
