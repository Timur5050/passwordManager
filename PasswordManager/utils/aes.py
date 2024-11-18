import base64

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os


class AesAlgorithm:
    def __init__(self):
        keys_folder = os.path.join("keys_aes")

        with open(os.path.join(keys_folder, "key.bin"), "rb") as key_file:
            key = key_file.read()

        with open(os.path.join(keys_folder, "iv.bin"), "rb") as iv_file:
            iv = iv_file.read()
        self.cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())

    def encode_aec_algorithm(self, message: str):
        encryptor = self.cipher.encryptor()
        ciphertext = encryptor.update(message.encode()) + encryptor.finalize()
        return base64.b64encode(ciphertext).decode("utf-8")

    def decode_aec_algorithm(self, ciphertext: str):
        ciphertext = base64.b64decode(ciphertext)
        decryptor = self.cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        return plaintext.decode()

aes = AesAlgorithm()
ac = aes.encode_aec_algorithm("Hello, world")

print(ac)
dec = aes.decode_aec_algorithm(ac)
print(dec)

