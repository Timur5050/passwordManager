import jwt
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

from user import router as user_router
from auth.utils import decode_jwt

app = FastAPI()

app.include_router(user_router.router)
