from typing import List

import bcrypt
import src.models.models as _models
from src.configs.database import db_dependency
from src.dto.index import LoginDto
from fastapi import HTTPException
from src.models.schema import StudentSchema


async def save_user(student: StudentSchema, db: db_dependency):
    # hashed_password = bcrypt.hashpw(student.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    db_student = _models.Student(
        student_id=student.student_id,
        email=student.email,
        name=student.name,
    )

    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    
    return db_student

async def login_service(login_dto: LoginDto, db: db_dependency):
    db_student = db.query(_models.Student).filter(_models.Student.student_id == login_dto.student_id).first()
    
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    db_student_password = db_student.password.encode('utf-8')
    if not bcrypt.checkpw(login_dto.password.encode('utf-8'), db_student_password):
        raise HTTPException(status_code=400, detail="Password incorrect")
    
    return {
        "id": db_student.id,
        "student_id": db_student.student_id,
        "name": db_student.name,
        "email": db_student.email,
    }
    
def get_students_service(db: db_dependency) -> List[StudentSchema]:
    students = db.query(_models.Student).all()
    return [StudentSchema(
        id=student.id,
        student_id=student.student_id,
        name=student.name,
        email=student.email
    ) for student in students]