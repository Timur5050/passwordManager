import base64
import os

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

from cryptography.hazmat.primitives import serialization


class RsaAlgorithm:
    def __init__(self):
        keys_folder = os.path.join("keys_rsa")

        with open(os.path.join(keys_folder, "private_key.pem"), "rb") as key_file:
            pem_private_key = key_file.read()

        with open(os.path.join(keys_folder, "public_key.pem"), "rb") as iv_file:
            pem_public_key = iv_file.read()

        self.private_key = serialization.load_pem_private_key(
            pem_private_key,
            password=None
        )
        self.public_key = serialization.load_pem_public_key(pem_public_key)

    def encode_res_algorithm(self, message: str):
        message = message.encode()

        ciphertext = self.public_key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return base64.b64encode(ciphertext).decode('utf-8')

    def decode_res_algorithm(self, ciphertext: str):
        ciphertext = base64.b64decode(ciphertext)

        decrypted_bytes = self.private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return decrypted_bytes.decode('utf-8')
