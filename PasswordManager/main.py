from fastapi import FastAPI

from passwords.router import router as password_router

app = FastAPI()


app.include_router(router=password_router)
