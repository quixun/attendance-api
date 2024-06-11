from pydantic import BaseModel


class StudentSchema(BaseModel):
    student_id: str
    email: str
    name: str