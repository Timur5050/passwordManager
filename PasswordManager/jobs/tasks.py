from datetime import datetime

from celery_app import celery_app
from dependencies import get_db
from passwords.models import Password


@celery_app.task
def print_message():
    session = next(get_db())
    session.query(Password).filter(Password.delete_time < datetime.now()).delete(synchronize_session=False)
    session.commit()
    print("cleaning has been done")
