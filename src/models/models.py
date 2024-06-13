import uuid

from configs.database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, text
from sqlalchemy.orm import relationship


class Student(Base):
    __tablename__ = "students"

    id = Column(String, primary_key=True, nullable=False, default=lambda: str(uuid.uuid4()))
    student_id = Column(String, nullable=False)
    email = Column(String, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    
    attendances = relationship("Attendance", back_populates="student")


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(String, primary_key=True, nullable=False, default=lambda: str(uuid.uuid4()))
    thumbnail = Column(String, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    
    attendances = relationship("Attendance", back_populates="subject")


class Attendance(Base):
    __tablename__ = "attendances"

    id = Column(String, primary_key=True, nullable=False, default=lambda: str(uuid.uuid4()))
    student_id = Column(String, ForeignKey('students.id'), nullable=False)
    subject_id = Column(String, ForeignKey('subjects.id'), nullable=False)
    attended_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))

    student = relationship("Student", back_populates="attendances")
    subject = relationship("Subject", back_populates="attendances")
