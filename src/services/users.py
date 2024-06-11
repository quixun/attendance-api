import models.models as _models
from configs.database import db_dependency
from models.schema import StudentSchema


async def save_user(student: StudentSchema, db: db_dependency):
    db_student = _models.Student(student_id=student.student_id, email=student.email, name=student.name)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    print(db_student)
    
    return db_student