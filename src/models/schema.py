from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class StudentSchema(BaseModel):
    student_id: str
    email: str
    name: str

    class Config:
        orm_mode = True
        from_attributes = True

class SubjectSchema(BaseModel):
    id: str
    name: str
    thumbnail: str

    class Config:
        orm_mode = True
        from_attributes = True

class AttendanceSchema(BaseModel):
    id: Optional[str] = None
    student_id: str
    subject_id: str
    attended_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        from_attributes = True
