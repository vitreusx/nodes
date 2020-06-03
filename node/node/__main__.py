from .nexus import Nexus
from .net.installer import Installer as NetInst
from .voice.installer import Installer as VoiceInst
from .local.installer import Installer as LocalInst

if __name__ == '__main__':
    nx = Nexus()
    for inst in [NetInst, VoiceInst, LocalInst]:
        inst(nx)

    ssl_certs = (f"certs/{nx.conf['net']['name']}.pem", f"certs/{nx.conf['net']['name']}_key.pem")
    print(ssl_certs)
    nx.app.run(host='0.0.0.0', port=nx.conf.get('port') or 8080, threaded=True, 
               ssl_context = ssl_certs)
