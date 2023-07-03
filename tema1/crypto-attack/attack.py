import base64
from Crypto.Cipher import AES
BLOCK_SIZE = 32

def decrypt_aes(msg, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(msg)

shared = 8295470404756197179435629427418057937628547743937306629317394846678279378121
encoded_flag = "o+C/uUQ6uTtZ9jpI4sWVjfOPViK3TjOjgqK9t/JPxi/Q/Hq68a57fAq7JA8Gpg4KndziMGt/Cfdd\n5jYFYy6LXg=="
encrypted_flag = base64.decodebytes(encoded_flag.encode("ASCII"))
key = shared.to_bytes((shared.bit_length() + 7) // 8, byteorder='big')[0:BLOCK_SIZE]
msg = decrypt_aes(encrypted_flag, key)
print(msg)