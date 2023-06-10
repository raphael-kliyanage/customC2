# TP - Scanner de ports
# Version 0.2
# Auteur : Mathis THOUVENIN

# Librairie importée
import socket
import sys
import os
from datetime import datetime
import threading
import argparse


# Fonction pour nettoyer l'affichage
def clear():
    # subprocess.call('clear', shell=True)

    # OS Windows
    if os.name == 'nt':
        windows = os.system('cls')

    # OS UNIX
    else:
        unix = os.system('clear')


clear()
"""""
# Fonction arguments
def parse():

    # Initialisation des arguments
    parser = argparse.ArgumentParser(description='Spécifier une gamme de ports différente')

    # Ajout d'arguments
    parser.add_argument('-p', type=int, help='Port')


    parser.parse_args()
parse()
"""
# Host qu'on doit scanne
host = socket.gethostbyname(input("Entrer une IP ou un domaine : "))

open_ports = {}


# On vérifie les ports ouverts
def scan(ip, port, delay, open_ports):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(delay)
        result = sock.connect_ex((ip, port))

        if result == 0:
            open_ports[port] = 'Port ouvert'
        # sock.close()

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


# On scanne les ports en thread pour plus de rapidité
def run_scanner(host, delay, file):
    thread_list = []

    for port in range(1, 1025):
        thread = threading.Thread(target=scan, args=(host, port, delay, open_ports))
        thread_list.append(thread)

    for index in range(0, 1024):
        thread_list[index].start()

    for index in range(0, 1024):
        thread_list[index].join()

    for value in open_ports.items():
        print("Port ouvert : " + str(value))

        # On met dans le fichier les ports qui sont ouverts
        file.write("\nNombre port ouvert: " + str(value))


# Créer un fichier pour mettre les informations de la dates ainsi que les ports qui sont ouverts)
file = open("scanner-port.txt", "w")

# Vérifier l'heure + mettre en format
now = datetime.now()
current_time = now.strftime("%H:%M:%S")

# Affichage du host et la date de début du scanne
print("-" * 40)
print(f"Cible : {host}")
print(f"Début du scanne: {current_time}")
print("-" * 40)

# On écrit la date de début du scanne dans le fichier texte
file.write("Début du scanne: {}".format(current_time))

# On appel notre fonction qui scanne les ports avec le host que nous avons indiqué, la durée du scanne et mettre le résultat dans un fichier
run_scanner(host, 3, file)

# Affichage de la date de fin du scanne
print("-" * 40)
print(f"Fin du scanne: {current_time}")

# On écrit la date de fin du scanne dans le fichier texte
file.write("\nFin du scanne: {}".format(current_time))
print("-" * 40)
