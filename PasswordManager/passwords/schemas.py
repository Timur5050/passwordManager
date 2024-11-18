from datetime import datetime

from pydantic import BaseModel


class PasswordCreateSchema(BaseModel):
    user_id: int
    application_name: str
    encoded_password: str
    encryption_algorithm: str
    delete_time: datetime | None
    notes: str | None = None


class GetPasswordToApplication(BaseModel):
    encryption_algorithm: str
    encoded_password: str


class UpdatePasswordSchema(BaseModel):
    encoded_password: str
    delete_time: datetime | None
    encryption_algorithm: str
    updated_at: datetime


class GetPasswordSchema(BaseModel):
    id: int
    user_id: int
    application_name: str
    encoded_password: str
    encryption_algorithm: str
    created_at: datetime
    updated_at: datetime | None
    delete_time: datetime | None
    notes: str | None


class PasswordCreating(BaseModel):
    application_name: str
    password: str
    encryption_algorithm: str
    delete_time: datetime | None = None
    notes: str | None = None


class UpdatePasswordMeta(BaseModel):
    password: str
    delete_time: datetime | None = None
    encryption_algorithm: str | None = None
