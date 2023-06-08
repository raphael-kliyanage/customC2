# client_revershell
# Version 0.3
# Auteur : Raphaël KATHALUWA-LIYANAGE

# code pour comprendre comment fonctionne la librairie
# pour changer de répertoire dans le code final
import shutil
import os
import subprocess

pwd = os.getcwd()
print(pwd)
cmd = "cp cp.py cp1.py"
x = cmd.split()
print(x)
#shutil.copy2('cp.py', 'C:/Users/Raphaël/Documents/python/customC2/cp1.py')
""""
if x[0] == "cp":
    src = directory + " " + x[1]
    dst = directory + " " + x[2]
    shutil.copy(src, dst)
    print(f"File copied: {x[1]} as {x[2]}")
else:
    command = subprocess.Popen(x, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = command.communicate()
    if output:
        print(output.decode())
    if err:
        print(err.decode())
        """