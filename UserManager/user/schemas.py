from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    email: EmailStr
    password: str


class UserRetrieveSchema(BaseModel):
    id: int
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    date_joined: datetime
