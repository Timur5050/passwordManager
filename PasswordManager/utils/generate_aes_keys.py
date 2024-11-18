import os


def generate_aes_keys():
    keys_folder = os.path.join("..", "keys_aes")

    os.makedirs(keys_folder, exist_ok=True)

    key = os.urandom(32)
    iv = os.urandom(16)

    with open(os.path.join(keys_folder, "key.bin"), "wb") as key_file:
        key_file.write(key)

    with open(os.path.join(keys_folder, "iv.bin"), "wb") as iv_file:
        iv_file.write(iv)

    print("aes keys have been generated")


generate_aes_keys()
