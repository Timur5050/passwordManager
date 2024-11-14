import jwt
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi import BackgroundTasks

from database import AsyncSessionLocal
from settings import settings
from user import crud
from user.models import User
from user.schemas import UserSchema, UserRetrieveSchema
from dependencies import get_db
from auth.utils import get_password_hash, encode_jwt, decode_jwt, verify_password, generate_code
from auth.send_mails import send_mail
from auth.middleware import get_user_id
from auth import middleware

router = APIRouter(prefix="/users", tags=["users"])


class VerifyLoginRequest(BaseModel):
    email: str
    code: str


class JWTAccessToken(BaseModel):
    token: str


@router.post("/register/", response_model=UserRetrieveSchema)
def register_user(user: UserSchema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    password = get_password_hash(user.password)
    user.password = password

    return crud.create_user(
        db=db,
        user=user,
    )


def authenticate_user(email: str, password: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        return False
    if not verify_password(password, db_user.password):
        return False
    return db_user


@router.post("/verify/login/", response_model=None)
def verify_login_and_get_token(data: VerifyLoginRequest, db: Session = Depends(get_db)):
    email = data.email
    code = data.code
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=400, detail="no such user")
    key = f"2f{user.id}"
    redis_client = settings.redis.get_redis_client()
    value = redis_client.get(key)
    if value is None:
        raise HTTPException(status_code=400, detail="token expired")
    ttl = redis_client.ttl(key)
    if ttl <= 0:
        redis_client.delete(key)
        raise HTTPException(status_code=400, detail="token expired")
    value = value.decode('utf-8')
    if value != code:
        raise HTTPException(status_code=400, detail="token is invalid")

    if value:
        redis_client.delete(key)
    general_payload = {
        "email": user.email,
        "user_id": user.id,
    }

    access_payload = general_payload.copy()
    access_payload["token_type"] = "access"

    refresh_payload = general_payload.copy()
    refresh_payload["token_type"] = "refresh"

    access_token = encode_jwt(payload=access_payload)
    refresh_token = encode_jwt(payload=refresh_payload)

    response_content = {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }
    response = JSONResponse(response_content)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True
    )

    return response


@router.post("/login/", response_model=None)
async def login_user(
        user: UserSchema,
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db)
):
    user_in_db = authenticate_user(user.email, user.password, db)
    if not user_in_db:
        raise HTTPException(status_code=400, detail="Email or password incorrect")

    code = generate_code()

    background_tasks.add_task(send_mail, user_in_db.email, code)

    redis_client = settings.redis.get_redis_client()
    key = f"2f{user_in_db.id}"
    if redis_client.get(key):
        redis_client.delete(key)

    redis_client.set(key, code, ex=60)

    return {"verify": "we have sent a code to your email"}


@router.post("/token/refresh/", response_model=None)
async def refresh_old_token(request: Request):
    body = await request.json()
    refresh_token = body.get("refresh_token")
    try:
        payload = decode_jwt(refresh_token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token expired")

    new_payload = {
        "email": payload.get("email"),
        "user_id": payload.get("user_id"),
        "token_type": "access"
    }
    new_access_token = encode_jwt(payload=new_payload)
    response_content = {"access_token": new_access_token}

    response = JSONResponse(response_content)
    response.set_cookie(key="access_token", value=new_access_token, httponly=True, secure=True)

    return response


@router.get("/user_id/", response_model=None)
def get_user_id(request: Request):
    return middleware.get_user_id(request)


@router.get("/user_id_by_token/", response_model=None)
def get_user_id_by_the_token(token: JWTAccessToken):
    return {
        "user_id": middleware.get_user_id_by_the_token(
            token=token.token
        )
    }
