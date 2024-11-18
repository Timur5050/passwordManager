import os

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding


def generate_rsa_keys():
    keys_folder = os.path.join("..", "keys_rsa")

    os.makedirs(keys_folder, exist_ok=True)

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    pem_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    pem_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open(os.path.join(keys_folder, "private_key.pem"), "wb") as key_file:
        key_file.write(pem_private_key)

    with open(os.path.join(keys_folder, "public_key.pem"), "wb") as iv_file:
        iv_file.write(pem_public_key)

    print("rsa keys have been generated")


generate_rsa_keys()
