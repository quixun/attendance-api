from typing import List

from pydantic import BaseModel


class RegisterStudentDto(BaseModel):
    student_id: str
    email: str
    name: str
    photos: List[str]
    
class MarkAttendanceDto(BaseModel):
    student_id: str
    subject_id: str
class LoginDto(BaseModel):
    student_id: str
    password: str