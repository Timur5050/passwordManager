from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from database import Base


class Password(Base):
    __tablename__ = "passwords"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    application_name = Column(String)
    encoded_password = Column(String)
    encryption_algorithm = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, nullable=True)
    delete_time = Column(DateTime, nullable=True, index=True)
    notes = Column(String, nullable=True)
