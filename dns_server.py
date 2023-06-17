import time
from dnslib import DNSRecord, DNSHeader, QTYPE, A, RR
from dnslib.server import DNSServer, DNSHandler, BaseResolver
import base64

IP_REPLY = '1.2.3.4'
HOST = '0.0.0.0'
PORT = 53

class CustomResolver(BaseResolver):
    def resolve(self, request, handler):
        qname = request.q.qname
        qtype = request.q.qtype

        decoded_data_list = []  # Create an empty list to store the decoded data

        for label in qname.label[:-2]:
            encoded_data = label.decode()
            try:
                decoded_data = base64.b64decode(encoded_data).decode()
                decoded_data_list.append(decoded_data)

            except Exception as e:
                print(f"Error decoding label: {e}")

        reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)

        if qtype == QTYPE.A:
            reply.add_answer(RR(qname, qtype, rdata=A(IP_REPLY)))

        return reply, decoded_data_list

class CustomDNSHandler(DNSHandler):
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        request = DNSRecord.parse(data)
        reply, decoded_data_list = self.server.resolver.resolve(request, self)
        
        counter = 0
        try:
            for command in decoded_data_list:
                print(command, end="")
        except Exception as e:
            print(e)

        socket.sendto(reply.pack(), self.client_address)

if __name__ == "__main__":
    resolver = CustomResolver()
    server = DNSServer(resolver, port=PORT, handler=CustomDNSHandler)

    server.start()
