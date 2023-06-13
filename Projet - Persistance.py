# Persistence du script
# 0.5
# Auteur : Mathis THOUVENIN

# Librairie importée
import sys
import os
import shutil
import platform
import subprocess

# Initialisation des variables

# Emplacement d'origine du script
# path_source = os.path.abspath(__file__)
path_source = "/home/kali/Documents/Sécurité avec Python/TP - Scanneur de ports_1.py"

# Détection du système d'exploitation
system_os = platform.system()

# Emplacement de destination pour la duplication sur un windows [!] Attention au droit du dossier [!]
path_destination = {
    'Windows': 'C:/',
    'Linux': '/home/kali/Documents/'
}

# Mon script
my_script = os.path.basename(__file__)

# Emplacement du fichier de verrouillage
lock_file = "/home/kali/Documents/Sécurité avec Python/TP - Scanneur.lock"

# Fonction de fichier verrouillage
def lock():
    # Vérification si le fichier de verrouillage existe
    if os.path.exists(lock_file):
        print("Lock : Le script est déjà en cours d'exécution")
        # sys.exit()

    # Création du fichier de verrouillage
    else:
        print("Lock : Création du fichier de verrouillage")
        file_lock = open("TP - Scanneur.lock", "w")
        file_lock.write(str(os.getpid()))
        subprocess.Popen([sys.executable] + sys.argv)


lock()

# Suppression du fichier de verrouillage à la fin de l'exécution du script
# os.remove(lock_file)

# Fonction de reduplication
def reduplication():
    # On met une condition si le fichier n'existe pas
    if not os.path.exists(path_source):

        # On récupère l'emplacement de destination en fonction du système de l'exploitation
        paths = path_destination.get(system_os)

        if paths:
            # On duplique le script sur le nouvel emplacement
            copy_path = os.path.join(paths, my_script)
            shutil.copyfile(sys.argv[0], copy_path)

            # On affiche un message de confirmation
            print("Reduplication : Le script a été redupliqué avec succès dans cet emplacement : ", copy_path)

        # Autre qu'un système exploitation de la liste
        else:
            print("Reduplication : Système d'exploitation non pris en charge")

    # Si le fichier existe
    else:
        print("Reduplication : Le script s'exécute normalement")

reduplication()
