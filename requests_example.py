import requests

def get_requests_auth():
    return {'auth': ('local', 'NmWpaKopHrxqPagL'), 'verify': './certs/nodeA.crt'}


response = requests.get("https://127.0.0.1:8080/net/groups", **get_requests_auth())
print(response.content)