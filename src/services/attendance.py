import uuid
from datetime import datetime, timezone

from fastapi import HTTPException
from src.models.models import Attendance, Student, Subject
from src.models.schema import AttendanceSchema
from sqlalchemy.orm import Session
from sqlalchemy.sql import func


async def mark_attendance(mark_attendance: AttendanceSchema, db: Session):
    student = db.query(Student).filter(Student.student_id == mark_attendance.student_id).first()
    print(student)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    subject = db.query(Subject).filter(Subject.id == mark_attendance.subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    existing_attendance = db.query(Attendance).filter(
        Attendance.student_id == student.id,
        Attendance.subject_id == subject.id,
        func.date(Attendance.attended_at) == datetime.utcnow().date()
    ).first()
    
    if existing_attendance:
        raise HTTPException(status_code=400, detail="Attendance already marked for today")

    attendance = Attendance(
        id=str(uuid.uuid4()),
        student_id=student.id,
        subject_id=subject.id,
        attended_at=datetime.utcnow() 
    )

    # Lưu vào database
    db.add(attendance)
    db.commit()
    db.refresh(attendance)

def get_attended_students_by_subject_id(subject_id: str, db: Session):
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    attended_students = db.query(Student).\
        join(Attendance, Student.id == Attendance.student_id).\
        filter(Attendance.subject_id == subject_id).all()

    attended_student_dicts = [attendance_student_dicts(student, subject_id) for student in attended_students]
    
    return attended_student_dicts

def get_latest_attendance(student, subject_id):
    latest_attendance_time = datetime.min.replace(tzinfo=timezone.utc)

    for attendance in student.attendances:
        if attendance.subject_id == subject_id and attendance.attended_at > latest_attendance_time:
            latest_attendance_time = attendance.attended_at
    
    return latest_attendance_time

def attendance_student_dicts(student, subject_id):
    latest_attendance_time = get_latest_attendance(student, subject_id)
    
    return {
        "id": student.id,
        "student_id": student.student_id,
        "name": student.name,
        "email": student.email,
        "attended_at": latest_attendance_time if latest_attendance_time != datetime.min.replace(tzinfo=timezone.utc) else None
    }