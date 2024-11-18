from datetime import datetime

from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from dependencies import get_db
from passwords.utils import encode_password, decode_password

from passwords.models import Password
from passwords.schemas import PasswordCreateSchema, GetPasswordSchema, PasswordCreating, UpdatePasswordMeta, \
    UpdatePasswordSchema, GetPasswordToApplication
from passwords.utils import get_user_id_from_request
from passwords import crud

router = APIRouter(prefix="/passwords", tags=["passwords"])


@router.post("/", response_model=GetPasswordSchema)
def create_password(
        request: Request,
        password_info: PasswordCreating,
        db: Session = Depends(get_db)
):
    user_id = get_user_id_from_request(
        request=request
    )

    if db.query(Password).filter(
            Password.user_id == user_id,
            Password.application_name == password_info.application_name
    ).first():
        raise HTTPException(status_code=404, detail="you already have password for that app")

    encoded_password = encode_password(
        password=password_info.password,
        encryption_algorithm=password_info.encryption_algorithm
    )
    password = PasswordCreateSchema(
        user_id=user_id,
        application_name=password_info.application_name,
        encoded_password=encoded_password,
        encryption_algorithm=password_info.encryption_algorithm,
        delete_time=password_info.delete_time,
        notes=password_info.notes
    )
    return crud.create_password(
        db=db,
        password=password
    )


@router.put("/{password_id}", response_model=GetPasswordSchema)
def update_password(
        request: Request,
        password_id: int,
        update_password_data: UpdatePasswordMeta,
        db: Session = Depends(get_db)
):
    user_id = get_user_id_from_request(
        request=request
    )

    encryption_algorithm = update_password_data.encryption_algorithm
    if encryption_algorithm is None:
        password_to_update = db.query(Password).filter(Password.id == password_id).first()
        if password_to_update and password_to_update.user_id == user_id:
            encryption_algorithm = password_to_update.encryption_algorithm
        else:
            raise HTTPException(status_code=404, detail="no password with such id")

    encoded_password = encode_password(
        password=update_password_data.password,
        encryption_algorithm=encryption_algorithm
    )

    password_data = UpdatePasswordSchema(
        encoded_password=encoded_password,
        delete_time=update_password_data.delete_time,
        encryption_algorithm=encryption_algorithm,
        updated_at=datetime.now()
    )

    return crud.update_password(
        db=db,
        password_id=password_id,
        user_id=user_id,
        password_data=password_data
    )


@router.delete("/{password_id}", response_model=None)
def delete_password(
        request: Request,
        password_id: int,
        db: Session = Depends(get_db)
):
    user_id = get_user_id_from_request(
        request=request
    )
    res = crud.delete_password(
        db=db,
        password_id=password_id,
        user_id=user_id
    )
    if res:
        return JSONResponse(
            status_code=200,
            content={"message": "successfully deleted"}
        )

    return JSONResponse(
        status_code=404,
        content={"message": "password was not deleted"}
    )


@router.get("/{application_name}", response_model=GetPasswordToApplication)
def get_password_for_application(
        request: Request,
        application_name: str,
        db: Session = Depends(get_db)
):
    user_id = get_user_id_from_request(
        request=request
    )

    encoded_password_data = crud.get_password_by_application_name(
        db=db,
        application_name=application_name,
        user_id=user_id
    )
    if encoded_password_data is None:
        return JSONResponse(
            status_code=404, content={
                "message": "You do not have such password with such application name"
            }
        )
    decoded_password = decode_password(
        encoded_password=encoded_password_data.encoded_password,
        encryption_algorithm=encoded_password_data.encryption_algorithm
    )
    return JSONResponse(
        status_code=200, content={
            "password": decoded_password
        }
    )
