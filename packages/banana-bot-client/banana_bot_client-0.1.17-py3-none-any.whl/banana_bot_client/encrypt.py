import base64
import time

from Crypto.Cipher import AES
from Crypto.Hash import MD5
from Crypto.Random import get_random_bytes

PASSWORD = "1,1,0"


def evp_bytes_to_key(password, salt, key_len, iv_len):
    dtot = b""
    md5_hash = MD5.new()
    while len(dtot) < key_len + iv_len:
        md5_hash.update(dtot + password + salt)
        dtot += md5_hash.digest()
        md5_hash = MD5.new()
    return dtot[:key_len], dtot[key_len : key_len + iv_len]


def encrypt_request_time(timestamp=None):
    if timestamp is None:
        timestamp = int(time.time() * 1000)
    plaintext = str(timestamp).encode("utf-8")

    password = PASSWORD.encode("utf-8")
    salt = get_random_bytes(8)

    key_len = 32  # 256 bits
    iv_len = 16  # 128 bits

    key, iv = evp_bytes_to_key(password, salt, key_len, iv_len)

    pad_len = AES.block_size - len(plaintext) % AES.block_size
    padding = bytes([pad_len] * pad_len)
    padded_plaintext = plaintext + padding

    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(padded_plaintext)

    openssl_header = b"Salted__" + salt
    encrypted_data = openssl_header + ciphertext

    encoded = base64.b64encode(encrypted_data)
    return encoded.decode("utf-8")
