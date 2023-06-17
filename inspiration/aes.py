from hashlib import pbkdf2_hmac
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import Crypto.Protocol.KDF
import base64


KEY = b'W3c9vlwl1Cj0tM6FHkh3pZ%OTc+x8ET='
IV = b'efd6cb512023b721'

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
