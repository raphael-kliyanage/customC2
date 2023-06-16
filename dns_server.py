from dnslib import DNSRecord, DNSHeader, QTYPE, A, RR
from dnslib.server import DNSServer, DNSHandler, BaseResolver
import base64 
from Crypto.Cipher import AES
#from itertools import batched

IP_REPLY = '1.2.3.4'
HOST = '0.0.0.0'
PORT = 53

class CustomResolver(BaseResolver):
    def resolve(self, request, handler):
        qname = request.q.qname
        qtype = request.q.qtype

        for i in range(0, len(qname.label)-2):
            encoded_data = request.q.qname.label[i].decode()
            decoded_data = base64.b64decode(encoded_data).decode()

            print(f"{decoded_data}")
        
        reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)

        if qtype == QTYPE.A:
            reply.add_answer(RR(qname, qtype, rdata=A(IP_REPLY)))
            #reply.add_answer(*RR.fromZone(f"{qname} 1 TXT OK"))
    
        return reply

class CustomDNSHandler(DNSHandler):
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        request = DNSRecord.parse(data)
        reply = self.server.resolver.resolve(request, self)
        socket.sendto(reply.pack(), self.client_address)
    
if __name__ == "__main__":
    resolver = CustomResolver()
    server = DNSServer(resolver, port=PORT, handler=CustomDNSHandler)

    server.start()