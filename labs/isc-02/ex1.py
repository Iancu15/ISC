from Crypto.Cipher import AES
from Crypto import Random

BLOCK_SIZE = 32
PADDING = b'#'
iv = b"\x00" * 16

def decrypt(key, iv, data):
    aes = AES.new(key, AES.MODE_CBC, iv)
    data = aes.decrypt(data)
    return data

def pad(s):
    return s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING 

f = open("isc-lab02-secret.enc", "rb")
key = f.read(BLOCK_SIZE)
data = f.read()

dec = decrypt(key, iv, data)

f_out = open("secret.dec", 'wb')
f_out.write(dec)
f_out.close()
