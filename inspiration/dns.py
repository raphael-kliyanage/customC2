import dnslib
import socket
import base64 

# Replace with the IP address of the DNS server
dns_server = "8.8.8.8"

# Replace with the domain name and subdomain that you control
domain_name = "example.com"
subdomain = "tunnel"

# Replace with the data that you want to transfer
data = b"hello"

# Encode the data as a base64 string
encoded_data = base64.b64encode(data)

# Create a DNS query with the encoded data as the subdomain label
query = dnslib.DNSRecord.question(subdomain + "." + domain_name)

# Send the DNS query to the DNS server
dns_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dns_socket.sendto(query.pack(), (dns_server, 53))

# Receive the DNS response from the DNS server
response = dnslib.DNSRecord.parse(dns_socket.recv(4096))

# Decode the DNS response and extract the data payload
for i in range(0, 4096):
    results = []
    results = base64.b64decode(response)

    # Print the decoded data
    print(results[i])