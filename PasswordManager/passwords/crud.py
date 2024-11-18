from sqlalchemy.orm import Session

from passwords.models import Password
from passwords.schemas import PasswordCreateSchema, UpdatePasswordSchema, UpdatePasswordMeta


def create_password(db: Session, password: PasswordCreateSchema):
    password = Password(
        user_id=password.user_id,
        application_name=password.application_name,
        encoded_password=password.encoded_password,
        encryption_algorithm=password.encryption_algorithm,
        delete_time=password.delete_time,
        notes=password.notes
    )

    db.add(password)
    db.commit()
    db.refresh(password)

    return password


def update_password(
        db: Session,
        password_id: int,
        user_id,
        password_data: UpdatePasswordSchema
):
    password_to_update = db.query(Password).filter(Password.id == password_id).first()
    if password_to_update and password_to_update.user_id == user_id:
        password_to_update.encoded_password = password_data.encoded_password
        password_to_update.delete_time = password_data.delete_time
        password_to_update.encryption_algorithm = password_data.encryption_algorithm
        password_to_update.updated_at = password_data.updated_at

    db.commit()
    db.refresh(password_to_update)
    return password_to_update


def get_password_by_application_name(
        db: Session,
        application_name: str,
        user_id: int
) -> Password:
    return db.query(Password).filter(
        Password.application_name == application_name,
        Password.user_id == user_id
    ).first()


def delete_password(
        db: Session,
        password_id: int,
        user_id: int
):
    password_to_delete = db.query(Password).filter(
        Password.id == password_id
    ).first()
    print(password_to_delete)
    if password_to_delete and password_to_delete.user_id == user_id:
        db.delete(password_to_delete)
        db.commit()
        return True
    return False
