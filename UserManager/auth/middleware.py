import jwt
from fastapi import Request, HTTPException

from auth.utils import decode_jwt


def get_user_id_by_the_token(token: str) -> int:
    try:
        content = decode_jwt(token)
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Expired token")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    return content["user_id"]


def get_user_id(request: Request):
    headers = request.headers
    try:
        token = headers.get("Authorization").replace("Bearer ", "")
    except (KeyError, AttributeError):
        raise HTTPException(status_code=400, detail="Invalid Authorization header")

    return get_user_id_by_the_token(token)
