# code pour comprendre comment fonctionne la librairie
# pour changer de répertoire dans le code final
import os
import subprocess

cmd = "cd C:/Users"
x = cmd.split()

if x[0] == "cd" or x[0] == "dir":
    os.chdir(x[1])
    print("changed directory to {}".format(x[1]))
    command = subprocess.Popen('ipconfig',shell=True,stdout=subprocess.PIPE)
    output, err = command.communicate()
else:
    print(x)