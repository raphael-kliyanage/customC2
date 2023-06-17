from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

KEY = b'277EED85f4C6C65M'
IV = b'A5E8E95AF2723449'

def encrypt_aes_cbc(key, iv, plaintext):
    print(plaintext)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    print(ciphertext)
    return base64.b64encode(ciphertext).decode()

def decrypt_aes_cbc(key, iv, ciphertext):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(base64.b64decode(ciphertext))
    return unpad(decrypted_data, AES.block_size).decode()

print(encrypt_aes_cbc(KEY, IV, "hallo"))