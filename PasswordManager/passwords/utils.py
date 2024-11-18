import json

import httpx
from fastapi import Request, status
from fastapi.exceptions import HTTPException

from utils.aes import AesAlgorithm
from utils.rsa import RsaAlgorithm


def get_user_id_from_request(request: Request):
    token = get_token_from_request(request=request)
    request_to_get_user_id = httpx.post(
        "http://user_manager:8000/users/user_id_by_token/",
        json={"token": token}
    )
    if request_to_get_user_id.status_code != 200:
        raise HTTPException(status_code=400, detail="Expired or invalid token")

    user_id = json.loads(request_to_get_user_id.content).get("user_id")
    return user_id


def get_token_from_request(request: Request) -> str:
    headers = request.headers
    try:
        token = headers.get("Authorization").replace("Bearer ", "")
    except (KeyError, AttributeError):
        raise HTTPException(status_code=400, detail="Invalid Authorization header")

    return token


def encode_password(password: str, encryption_algorithm: str):
    encoded_password = None

    if encryption_algorithm == "AES":
        aes_encryption = AesAlgorithm()
        encoded_password = aes_encryption.encode_aec_algorithm(password)
    elif encryption_algorithm == "RSA":
        rsa_encryption = RsaAlgorithm()
        encoded_password = rsa_encryption.encode_res_algorithm(password)

    if encoded_password is None:
        raise HTTPException(status_code=400, detail="you should enter valid encryption algorithm, only RSA or AES")

    return encoded_password


def decode_password(encoded_password: str, encryption_algorithm):
    decoded_password = None
    if encryption_algorithm == "AES":
        aes_encryption = AesAlgorithm()
        decoded_password = aes_encryption.decode_aec_algorithm(encoded_password)
    elif encryption_algorithm == "RSA":
        rsa_encryption = RsaAlgorithm()
        decoded_password = rsa_encryption.decode_res_algorithm(encoded_password)

    if decoded_password is None:
        raise HTTPException(status_code=400, detail="you should enter valid encryption algorithm, only RSA or AES")

    return decoded_password
