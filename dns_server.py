from dnslib import DNSRecord, DNSHeader, QTYPE, A, RR
from dnslib.server import DNSServer, DNSHandler, BaseResolver
from base64 import b64decode

class CustomResolver(BaseResolver):
    def resolve(self, request, handler):
        qname = request.q.qname
        qtype = request.q.qtype

        print(f"Requête reçu pour {qname}")

        reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)

        if qtype == QTYPE.A:
            reply.add_answer(RR(qname, qtype, rdata=A('1.2.3.4')))
    
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
    server = DNSServer(resolver, port=1053, handler=CustomDNSHandler)

    server.start()
