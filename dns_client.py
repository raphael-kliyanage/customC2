from dns import resolver
import subprocess
import base64


def download_file(filename):
    file = open(filename, 'r')
    # Créer une instance de resolver
    res = resolver.Resolver()

    # Spécifier le serveur DNS
    res.nameservers = ['127.0.0.1']
    res.port = 1053

    # Faire une requête DNS
    answer = res.resolve("test.com", 'A')

    # Afficher la réponse
    for ipval in answer:
        print('IP', ipval.to_text())

download_file("persistance.py")