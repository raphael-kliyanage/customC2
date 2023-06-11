from dns import resolver
import subprocess
import base64

HOST = '192.168.1.6'
PORT = 53

# Créer une instance de resolver
res = resolver.Resolver()

# Spécifier le serveur DNS
res.nameservers = [HOST]
res.port = PORT

# Faire une requête DNS
answer = res.resolve("test.com", 'A')

# Afficher la réponse
for ipval in answer:
    print('IP', ipval.to_text())