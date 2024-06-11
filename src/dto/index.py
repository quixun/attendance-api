from typing import List

from pydantic import BaseModel


class RegisterStudentDto(BaseModel):
    student_id: str
    email: str
    name: str
    photos: List[str]