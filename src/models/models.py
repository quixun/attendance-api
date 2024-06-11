import uuid

from configs.database import Base
from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, text


class Student(Base):
    __tablename__ = "students"

    id = Column(String,primary_key=True, nullable=False, default=str(uuid.uuid4()))
    student_id = Column(String, nullable=False)
    email = Column(String,nullable=False)
    name = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))