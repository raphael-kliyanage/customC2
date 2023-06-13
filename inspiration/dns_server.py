from dnslib import DNSRecord, DNSHeader, QTYPE, A, RR
from dnslib.server import DNSServer, DNSHandler, BaseResolver
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# AES encryption/decryption functions
def encrypt(plaintext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return base64.b64encode(ciphertext).decode()

def decrypt(ciphertext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(base64.b64decode(ciphertext))
    return unpad(decrypted, AES.block_size).decode()

# Custom DNS resolver
class MyResolver(BaseResolver):
    def resolve(self, request, handler):
        # Extract the query name and type
        qname = str(request.q.qname)
        qtype = QTYPE[request.q.qtype]

        # Check if the query type is A
        if qtype == "A":
            # Decrypt the query name (assuming it's encrypted)
            decrypted_qname = decrypt(qname, "my_secret_key")

            # Perform DNS resolution with the decrypted query name
            resolved_ip = "1.2.3.4"  # Replace with your actual resolution logic

            # Encrypt the resolved IP before sending the response
            encrypted_ip = encrypt(resolved_ip, "my_secret_key")

            # Create the DNS response
            reply = request.reply()
            reply.add_answer(RR(qname=request.q.qname, rtype=A, rdata=A(encrypted_ip)))
            return reply

        # If the query type is not A, return an empty response
        return request.reply()

# Create a DNS server with the custom resolver
resolver = MyResolver()
server = DNSServer(resolver)

# Start the DNS server
server.start()
