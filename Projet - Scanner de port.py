# TP - Scanner de ports
# Version 0.1
# Auteur : Mathis THOUVENIN

# Librairie importée
import socket
import subprocess
import sys
import os
from datetime import datetime
import threading
from queue import Queue
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


# Fonction arguments
def parse():
    # Initialisation des arguments
    parser = argparse.ArgumentParser(description='Spécifier une gamme de ports différente')

    # Ajout d'arguments
    parser.add_argument('-p', type=int, help='Port')

    parser.parse_args()


parse()
# Host qu'on doit scanne
host = socket.gethostbyname(input("Entrer une IP ou un domaine : "))

# Vérifier l'heure + mettre en format
now = datetime.now()
current_time = now.strftime("%H:%M:%S")

# Affichage du host et de l'heure
print("-" * 40)
print(f"Cible : {host}")
print(f"Début du scanne: {current_time}")
print("-" * 40)


# Scanne des ports
def scan():
    try:
        for port in range(1, 1024):

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((host, port))

            if result == 0:
                print(f"Port ouvert", port)
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


scan()
queue = Queue()
open_ports = []


def worker():
    while not queue.empty():
        port = queue.get()
        if scan():
            print("Port ouvert:", port)
            open_ports.append(port)


def run_scanner(threads):
    thread_list = []

    for t in range(threads):
        thread = threading.Thread(target=worker)
        thread_list.append(thread)

    for thread in thread_list:
        thread.start()
        thread.join()

    # for thread in thread_list


run_scanner(1021)
print(f"Scanneur complet dans : {current_time}")