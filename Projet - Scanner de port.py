# TP - Scanner de ports
# Version 0.5
# Auteur : Mathis THOUVENIN

# Librairie importée
import socket
import subprocess
import sys
import os
from datetime import datetime
import threading
import argparse
import pyfiglet


# Fonction pour nettoyer l'affichage
def clear():
    subprocess.call('clear', shell=True)

    # OS Windows
    if os.name == 'nt':
        windows = os.system('cls')

    # OS UNIX
    else:
        unix = os.system('clear')


clear()


# Fonction arguments en ligne de commande
def parser():
    # Initialisation des arguments
    parser = argparse.ArgumentParser(description='Spécifier une gamme de ports différente')

    # Ajout d'arguments port étendu (autre que 1-1024)
    parser.add_argument('-e', '--extend', dest='extend', action="store_true", help='Scan de port à partir de 1024')

    # Ajout d'arguments pour ne pas utiliser le ping
    parser.add_argument('-wp', '--without_ping', dest='without_ping', action="store_false",
                        help='sans utiliser le ping')

    return parser.parse_args()


# Fonction pour mettre une bannière
def banner():
    # Définition que de qu'on veut mettre comme bannière
    scan_banner = pyfiglet.figlet_format("SCAN DE PORT")

    # Affichage de la bannière
    print(scan_banner)

    return banner


# Dictionnaire pour les bannières de services
services_banners = {
    20: "FTP Transmission",
    21: "FTP Connexion",
    22: "SSH/SFTP",
    23: "Telnet",
    25: "SMTP",
    43: "WHOIS",
    53: "DNS",
    80: "HTTP",
    88: "Kerberos",
    110: "POP3",
    115: "SFTP",
    143: "IMAP",
    389: "LDAP",
    443: "HTTPS",
    514: "Shell",
    636: "LDAPS",
    992: "Telnets",
    993: "IMAPS",
    995: "POP3S",
    2049: "NFS",
    3306: "mysql"
}

# Appel de la fonction bannière
print("-" * 40)
banner()
print("-" * 40)

# Host qu'on doit scan
host = socket.gethostbyname(input("Entrer une IP ou un domaine : "))

args = parser()

open_ports = {}

# Tentative de prendre la bannière des services
"""
def get_banner(ip, port):

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((ip, port))
        banner = sock.recv(1024).decode().strip()
        sock.close()
        return banner

    except socket.timeout:
        return "Timeout"

    except ConnectionRefusedError:
        return "Connexion refusée"

    except:
        return "Erreur"
"""


# On vérifie les ports ouverts
def check_scan(ip, port, delay, open_ports):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(delay)
        result = sock.connect_ex((ip, port))

        if result == 0:
            # Tentative d'introduire les bannières de services
            """banner = get_banner(ip, port)

            if port in services_banners:
                service = services_banners[port]

            else:
                service = "Service inconnu

            open_ports[port] = {
                'service': service,
                'banner': banner
            }"""
            open_ports[port] = 'Ouvert'
            sock.close()

    # Gestion d'erreurs
    except KeyboardInterrupt:
        print(" Interruption")
        sys.exit()

    except socket.gaierror:
        print("Host pas trouvé")
        sys.exit()

    except socket.error:
        print("Pas pu se connecter sur la machine")
        sys.exit()


# On scan les ports en thread pour plus de rapidité
def run_scan(host, delay, file):
    thread_list = []

    # Si on n'utilise pas d'argument pour une plage de port différente que 1 à 1025
    if args.extend == False:

        for port in range(1, 1025):
            thread = threading.Thread(target=check_scan, args=(host, port, delay, open_ports))
            thread_list.append(thread)

        for index in range(0, 1024):
            thread_list[index].start()

        for index in range(0, 1024):
            thread_list[index].join()

        # Tentative d'ajouter l'affichage avec les bannières de services
        """for port in open_ports:
            service = open_ports[port]['service']
            banner = open_ports[port]['banner']
            print(f"Port {port} ({service}) est ouvert. Bannière : {banner}")"""

        for value in open_ports.items():
            print("Port ouvert : " + str(value))

            # On met dans le fichier les ports qui sont ouverts
            file.write("\nNombre port ouvert: " + str(value))

    # Si on utilise l'argument pour une plage de port différente de 1026 à 5000
    else:
        # A les utiliser s'il faut que l'utilisateur choissise la plage de port
        # start_port = int(input("Veuillez renseigner le port par lequel le scan commence : "))
        # end_port = int(input("Veuillez renseigner le port par lequel le scan se termine : "))

        for port in range(1026, 65000):
            thread = threading.Thread(target=check_scan, args=(host, port, delay, open_ports))
            thread_list.append(thread)

        for index in range(1025, 5000):
            thread_list[index].start()

        for index in range(1025, 5000):
            thread_list[index].join()

        for value in open_ports.items():
            print("Port ouvert : " + str(value))

            # On met dans le fichier les ports qui sont ouverts
            file.write("\nNombre port ouvert: " + str(value))


# Créer un fichier pour mettre les informations de la date ainsi que les ports qui sont ouverts
file = open("scanner-port.txt", "w")

# Vérifier l'heure + mettre en format
now = datetime.now()
current_time = now.strftime("%H:%M:%S")

# Affichage du host et la date de début du scan
print("-" * 40)
print(f"Cible : {host}")
print(f"Début du scan: {current_time}")
print("-" * 40)

# On écrit la date de début du scan dans le fichier texte
file.write("Début du scan: {}".format(current_time))

# On appel notre fonction qui scan les ports
run_scan(host, 5, file)

# Affichage de la date de fin du scan
print("-" * 40)
print(f"Fin du scan: {current_time}")

# On écrit la date de fin du scan dans le fichier texte
file.write("\nFin du scan: {}".format(current_time))
print("-" * 40)
