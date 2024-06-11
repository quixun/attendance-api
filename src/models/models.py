from configs.database import Base
from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, text


class Student(Base):
    __tablename__ = "students"

    id = Column(String,primary_key=True, nullable=False)
    email = Column(String,nullable=False)
    name = Column(String,nullable=False)
    published = Column(Boolean, server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))