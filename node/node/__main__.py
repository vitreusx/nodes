from .nexus import Nexus
from .net.installer import Installer as NetInst
from .voice.installer import Installer as VoiceInst
from .local.installer import Installer as LocalInst

if __name__ == '__main__':
    nx = Nexus()
    for inst in [NetInst, VoiceInst, LocalInst]:
        inst(nx)
    nx.app.run(host='0.0.0.0', port=nx.conf.get('port') or 8080, threaded=True)
